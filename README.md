# circuitpython.cookbook


## Build a circuitpython devel virtual env

CircuitPython-stubs is a collection of type hints for the CircuitPython library. It provides type annotations for the functions, classes, and variables defined in CircuitPython, which can help you write more accurate and maintainable Python code.

```bash
# new virtual env
python -m venv venv
source venv/bin/activate
# add circuitPython-stubs and configure it for a specific board
pip install circuitpython-stubs
circuitpython_setboard raspberry_pi_pico
# let's add some libraries used with our projects
pip install adafruit-circuitpython-hid
```

more info: https://learn.adafruit.com/welcome-to-circuitpython/pycharm-and-circuitpython#install-circuitpython-stubs-3105091