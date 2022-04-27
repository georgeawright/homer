# Linguoplotter

Linguoplotter is a cognitive model of language generation. It describes data using concepts and frames in a concept network.

## Setup

Linguoplotter is set-up with a dictionary of loggers and an optional random seed:

```python
    linguoplotter = Linguoplotter.setup(loggers, random_seed=1)
```

Loggers included in the `loggers` dictionary should be "activity", "structure", and "errors".

Default loggers are implemented in `Linguoplotter.loggers`

## Providing Knowledge

Linguoplotter includes an interpreter for a LISP-like language that can be used to define concepts, frames, and letter-chunks in a concept network.

```python
    with open("program.lisp", "r") as f:
        program = f.read()
        narrator.run_program(program)
```