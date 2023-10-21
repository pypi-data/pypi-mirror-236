import argparse
import contextlib
import dataclasses
import datetime
import itertools
import json
import os
import pathlib
import shlex
import sys
import typing

import psutil
import yaml
from pydantic import ValidationError
from pydantic import dataclasses as py_dataclasses

from . import run_proc, slurm_utils
from .dry_run import DryRun
from .parser_utils import RunExpState, add_runexp_args, remove_runexp_args


class TypedDictLike(typing.Protocol):
    "something that can be constructed with kwargs"


T = typing.TypeVar("T")

Fun: typing.TypeAlias = typing.Callable[[TypedDictLike], None]


def typed_dict_like(cls: type) -> typing.TypeGuard[type[TypedDictLike]]:
    if py_dataclasses.is_pydantic_dataclass(cls):
        return True
    if dataclasses.is_dataclass(cls):
        return True
    if issubclass(cls, dict | tuple):
        return bool(typing.get_type_hints(cls))
    return False


def to_dict(item: TypedDictLike) -> dict[str, typing.Any]:
    if dataclasses.is_dataclass(item):
        return dataclasses.asdict(item)
    if isinstance(item, dict):
        return item
    if isinstance(item, tuple):
        hints = typing.get_type_hints(type(item))
        return {key: getattr(item, key) for key in hints}
    raise TypeError(f"{type(item)=!r} not supported")


def sanitize(fun) -> tuple[Fun, type[TypedDictLike], str | None]:
    "sanitize function and return data type and documentation"

    hints = typing.get_type_hints(fun)
    arg_hints = {k: v for k, v in hints.items() if k != "return"}
    if len(arg_hints) != 1:
        raise ValueError(f"{fun} should take exactly 1 parameters (hints: {hints})")
    dtype: type = next(iter(arg_hints.values()))

    if not typed_dict_like(dtype):
        raise TypeError(f"{dtype} is not a supported type")

    doc: str | None = fun.__doc__

    def _tp_check(fn) -> typing.TypeGuard[Fun]:
        return True

    assert _tp_check(fun)

    return fun, dtype, doc


def read_config(config: str):
    "read the config file at the given path"

    config_path = pathlib.Path(config)
    if not config_path.is_file():
        raise ValueError(f"{config_path=!r} must be a file")

    with open(config_path, "r", encoding="utf8") as config_file:
        match config_path.suffix.lower():
            case ".yml":
                return yaml.safe_load(config_file)
            case ".yaml":
                return yaml.safe_load(config_file)
            case ".json":
                return json.load(config_file)
            case _:
                raise ValueError(f"unrecognized format: {config_path.suffix!r}")


def write_config(value: TypedDictLike, path: pathlib.Path):
    if path.exists():
        raise ValueError(f"will not override {path!r}")

    # correct format
    value = {"base_config": to_dict(value)}

    with open(path, "w", encoding="utf8") as config_file:
        match path.suffix.lower():
            case ".yml":
                yaml.safe_dump(value, config_file)
            case ".yaml":
                yaml.safe_dump(value, config_file)
            case ".json":
                json.dump(value, config_file)
            case _:
                raise ValueError(f"unrecognized format: {path.suffix!r}")


def prep_parser(parser: argparse.ArgumentParser):
    parser.add_argument("config_file", type=str, help="JSON/YAML file with the config")
    add_runexp_args(parser)


def get_args(doc: str | None, cli: list[str] | None = None):
    # build CLI to run this function
    parser = argparse.ArgumentParser(
        description=doc,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    prep_parser(parser)
    return parser.parse_args(cli)


def assess_mutually_exclusive(
    base_config: dict[str, typing.Any], sweep_groups: list[dict[str, list]]
):
    if not sweep_groups:
        return

    seen_keys = set(base_config.keys())

    for group_ in sweep_groups:
        for key, val in group_.items():
            if key in base_config:
                raise ValueError(f"overriding base_config.{key} is not allowed")
            if not isinstance(val, (list, tuple)):
                raise ValueError(
                    f"sweep.{key} should be a list or tuple, found: {val!r}"
                )
            if key in seen_keys:
                raise ValueError(f"another sweep group already uses {key}")
            seen_keys.add(key)


def reverse_zip(sweep_group: dict[str, list]):
    cfg_list: list[dict[str, typing.Any]] = []

    if not sweep_group:
        return cfg_list

    # check for length and prohibit overriding
    common_length = 0
    for key, val in sweep_group.items():
        if not common_length:
            common_length = len(val)
        elif len(val) != common_length:
            raise ValueError(
                f"len(sweep.{key})={len(val)} mismatch with previous "
                f"sweep options (len(prev)={common_length})"
            )

    if not common_length:
        raise ValueError("empty sweep are not allowed")

    for idx in range(common_length):
        cfg: dict[str, typing.Any] = {}
        for key, val_lst in sweep_group.items():
            cfg[key] = val_lst[idx]
        cfg_list.append(cfg)

    return cfg_list


def iter_sweep(
    base_cfg: dict[str, typing.Any], sweep_groups: list[list[dict[str, typing.Any]]]
):
    sweep_items: tuple[dict[str, typing.Any], ...]
    for sweep_items in itertools.product(*sweep_groups):
        copy = {**base_cfg}

        for sweep_dict in sweep_items:
            copy.update(sweep_dict)

        yield copy


def repr_call(fun: Fun, config: TypedDictLike):
    return f"calling {fun.__name__}({config!r})"


def run_no_sweep(
    fun: Fun,
    config: TypedDictLike,
    config_path: str,
    state: RunExpState,
):
    if not state.use_slurm:
        if state.no_dry_run:
            fun(config)
        else:
            DryRun().print(repr_call(fun, config))
        return

    command_list = [sys.executable] + remove_runexp_args(
        psutil.Process(os.getpid()).cmdline()[1:]
    )

    slurm_utils.run_slurm(
        state.template_file,
        config_path,
        fun.__name__,
        command_list,
        state.slurm_args,
        state.no_dry_run,
    )


def run_sweep(
    fun: Fun,
    config_list: list[TypedDictLike],
    config_path: str,
    state: RunExpState,
):
    now = datetime.datetime.now()

    if not state.use_slurm:
        if state.no_dry_run:
            run_proc.run(fun, config_list, max_concurrency=state.max_concurrent_proc)
        else:
            run = DryRun()
            for cfg in config_list:
                run.print(repr_call(fun, cfg))
        return

    if state.template_file is None:
        raise ValueError("slurm sweep are only implemented with template files")

    command_list = [sys.executable] + remove_runexp_args(
        psutil.Process(os.getpid()).cmdline()[1:]
    )
    path_idx = command_list.index(config_path)

    with contextlib.ExitStack() as stack:
        # create all config-now-\d.yml for \d=1-10 (make sure this format is exact)
        config_path_ = pathlib.Path(config_path)
        config_prefix = config_path_.stem + f"_{now.isoformat()}"
        for idx, config in enumerate(config_list):
            path_ = config_path_.with_stem(config_prefix + f"-{1 + idx}")
            write_config(config, path_)

            # remove in dry-run
            if not state.no_dry_run:
                stack.callback(path_.unlink)

        command_list[path_idx] = str(config_path_.with_stem(config_prefix + r"-%a"))
        command = shlex.join(command_list)

        slurm_utils.run_from_template(
            state.template_file,
            slurm_utils.job_path(config_path, now.isoformat()),
            state.no_dry_run,
            fun.__name__,
            command,
            state.slurm_args,
            sbatch_options=[
                f"#SBATCH --array=1-{len(config_list)}%{state.max_concurrent_proc}"
            ],
        )


C = typing.TypeVar("C", bound=TypedDictLike)


def try_cast(value: dict[str, typing.Any], dtype: typing.Type[C]):
    try:
        return dtype(**value)
    except (TypeError, ValidationError) as exc:
        raise ValueError("invalid config") from exc


def _runexp_body(fun: Fun, dtype: type[TypedDictLike], args: argparse.Namespace):
    runexp_state = RunExpState.pop_state(args)

    # read config
    config_data = read_config(args.config_file)
    try:
        base_config: dict[str, typing.Any] = config_data["base_config"]
    except KeyError:
        raise ValueError(f"config at {args.config_file} should have a 'base_config'")

    # find sweep options
    sweep_groups: list[dict[str, typing.Any]] = config_data.get("sweep", [])
    assess_mutually_exclusive(base_config, sweep_groups)
    sweep_factors = [reverse_zip(group) for group in sweep_groups]

    if not sweep_factors:
        config = try_cast(base_config, dtype)
        run_no_sweep(fun, config, args.config_file, runexp_state)
        return

    run_sweep(
        fun,
        [try_cast(sweep, dtype) for sweep in iter_sweep(base_config, sweep_factors)],
        args.config_file,
        runexp_state,
    )


def _runexp_dec(fun_: T) -> T:
    """Use `fun`: as an entry point

    - fun: (python dataclass | pydantic dataclass | NamedTuple | TypedDict) -> None
    """
    fun, dtype, doc = sanitize(fun_)

    args = get_args(doc)
    _runexp_body(fun, dtype, args)

    return fun_


@typing.overload
def runexp_main() -> typing.Callable[[T], T]:
    ...


@typing.overload
def runexp_main(fun: T) -> T:
    ...


def runexp_main(fun: T | None = None) -> T | typing.Callable[[T], T]:
    """Use `fun`: as an entry point

    - fun: (python dataclass | pydantic dataclass | NamedTuple | TypedDict) -> None
    """

    if fun is None:
        return _runexp_dec
    return _runexp_dec(fun)


def runexp_multi(
    *named_commands,
    description: str | None = None,
    **kw_commands,
):
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parsers = parser.add_subparsers(title="actions")

    commands: dict[str, typing.Any] = {
        **{fn.__name__: fn for fn in named_commands},
        **kw_commands,
    }

    actions: dict[str, tuple[Fun, type[TypedDictLike], typing.Any]] = {}

    for key, fun_ in commands.items():
        fun, dtype, doc = sanitize(fun_)
        actions[key] = (fun, dtype, fun_)

        sub_parser = sub_parsers.add_parser(key, description=doc)
        sub_parser.set_defaults(key=key)

        prep_parser(sub_parser)

    args = parser.parse_args()
    fun, dtype, fun_ = actions[args.key]
    delattr(args, "key")

    _runexp_body(fun, dtype, args)
    return fun_
