# -*- coding: utf-8 -*-
from typing import Tuple, Optional

import pytest

import json
import socketio

from _pytest.nodes import Item
from _pytest.runner import CallInfo


def pytest_addoption(parser):
    group = parser.getgroup('immediate')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2020',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')



uri = "ws://localhost:9001"
sio = socketio.Client()
sio.connect(uri)


@pytest.hookimpl()
def pytest_runtest_logreport(report):
    sio.emit("testreport", { "id": report.nodeid, "when": report.when, "outcome": report.passed })

@pytest.hookimpl()
def pytest_sessionfinish():
    sio.disconnect()



@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
