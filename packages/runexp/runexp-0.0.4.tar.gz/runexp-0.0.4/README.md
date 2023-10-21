# runexp

Library to run experiment from argparse or config file with slurm

## Roadmap

- [X] ConfigFile
- [ ] ArgParse
  - [X] FIX: empty arguments raises an error
  - [X] FIX: bool flag with False default are incorrectly ignored
  - [X] FIX: over quoting some value
  - [X] FIX: pickle error on lambda function
- [X] Clarify the behavior inconsistance (see below)

### Behavior inconsistance

What should happen if no runexp option is given ?

For the ArgParse case, it makes sense that if no RunExp option is found, nothing happens : RunExp should be minimally intrusive and avoid breaking everything, so args are returned as if RunExp did nothing.

For the ConfigFile case, it is not possible to run the program without RunExp as this is the way to parse the config. If it makes sense to re-use the function, it should be defined elsewhere and the decorator should be used as a function.

Moreover, because the ArgParse function needs to return the namespace, it should exit the process on a dry run, while the ConfigFile currently doesn't.
