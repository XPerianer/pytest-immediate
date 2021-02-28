# pytest-immediate
[![Build Status](https://travis-ci.com/XPerianer/pytest-immediate.svg?token=zxZSSKHDHsHfpBmXtyLc&branch=main)](https://travis-ci.com/XPerianer/pytest-immediate)

A plugin helping to get immediate feedback with pytest. Reordering + report of errors using websockets.
It is part of the [ImmediateTestFeedback](https://github.com/XPerianer/ImmediateTestFeedback) ecosystem,
allowing [TestingBackend](https://github.com/XPerianer/TestingBackend) to execute test prioritized and with direct test feedback after failures.


## Features

- Reorder Tests pre-execution
- Get immediatly notified via SocketIO if tests fail

## Requirements

```
    'pytest>=6.1.2',
    'python-socketio>=5.0.0'
```

## Installation

It's best to do this in a virtual environment.
Activate it, and then run
```
git clone https://github.com/XPerianer/pytest-immediate.git
cd pytest-immediate
pip install . -r requirements.txt
```
You can check if the tools if working if you run pytest.
Under "plugins", it should mention ```immediate```.

## Usage

This plugin implements two main additional options for running pytest:
- ```--send-reports``` This enables the Socket.IO client to send data
- ```--test-ordering``` This takes an array of test names, and reorders the tests in the given orders.

For examples, see also the ```tests/test_immediate.py``` files, they show how both behave.

### Additional Parameters:
- ```--remote-connection--address``` additionally allows you to set the destination for the Socket.IO client. It defaults to ```ws://localhost:9001```


## License
Distributed under the terms of the `MIT`_ license, "pytest-immediate" is free and open source software

## Thanks
This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.
