# -*- coding: utf-8 -*-
from typing import List

import pytest

import json
import socketio

from _pytest.nodes import Item
from flask import Config
from requests import Session


def pytest_addoption(parser):
    group = parser.getgroup('immediate')
    group.addoption(
        '--test_ordering',
        action='store',
        dest='test_ordering',
        default='[]',
        help='Set the ordering of the tests, by the name of the test'
    )

    # parser.addini('HELLO', 'Dummy pytest.ini setting')


uri = "ws://localhost:9001"
sio = socketio.Client()
sio.connect(uri)


@pytest.hookimpl()
def pytest_runtest_logreport(report):
    sio.emit("testreport", {"id": report.nodeid, "when": report.when, "outcome": report.passed})


@pytest.hookimpl()
def pytest_sessionfinish():
    sio.disconnect()


# TODO this is ugly hardcoded, as well as should not be global. The function might be fixed with currying
max_test_index = 100000
test_indexes = {}


def get_test_index(test):
    test_name = test.nodeid
    if test_name in test_indexes:
        return test_indexes[test_name]
    return max_test_index


@pytest.hookimpl()
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]):
    test_ordering = json.loads(config.option.test_ordering)
    print(test_ordering)
    for index, test_name in enumerate(test_ordering):
        test_indexes[test_name] = index

    items.sort(key=get_test_index)
    for i in items:
        print(i)


uri = "ws://localhost:9001"
sio = socketio.Client()
sio.connect(uri)


@pytest.hookimpl()
def pytest_runtest_logreport(report):
    sio.emit("testreport", {"id": report.nodeid, "when": report.when, "outcome": report.passed})


@pytest.hookimpl()
def pytest_sessionfinish():
    sio.disconnect()


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
