# -*- coding: utf-8 -*-
from typing import List

import pytest

import json
import socketio

from _pytest.nodes import Item


def pytest_addoption(parser):
    group = parser.getgroup('immediate')
    group.addoption(
        '--test-ordering',
        action='store',
        dest='test_ordering',
        default='[]',
        help='Set the ordering of the tests, by the name of the test'
    )

    group.addoption(
        '--send-results',
        action='store_true',
        dest='send_reports',
        default=False,
        help='Send the test reports to the server'
    )

    group.addoption(
        '--remote-connection-address',
        action='store',
        dest='remote_connection_address',
        default='ws://localhost:9001',
        help='Set the remote address. Defaults to ws://localhost:9001'
    )

    # parser.addini('HELLO', 'Dummy pytest.ini setting')


sio = None


def setup_server(sio):
    uri = saved_config_options.remote_connection_address
    sio = socketio.Client()
    sio.connect(uri)


@pytest.hookimpl()
def pytest_runtest_logreport(report):
    if saved_config_options.send_results:
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
def pytest_collection_modifyitems(session, config, items: List[Item]):
    global saved_config_options
    saved_config_options = config.option
    test_ordering = json.loads(config.option.test_ordering)
    print(test_ordering)
    test_indexes.clear()
    for index, test_name in enumerate(test_ordering):
        if test_name in test_indexes:
            continue
        test_indexes[test_name] = index

    items.sort(key=get_test_index)
    for i in items:
        print(i)

    if config.option.send_reports:
        setup_server(sio)


@pytest.hookimpl()
def pytest_runtest_logreport(report):
    if saved_config_options.send_reports:
        sio.emit("testreport", {"id": report.nodeid, "when": report.when, "outcome": report.passed})


@pytest.hookimpl()
def pytest_sessionfinish():
    print("Disconnect")
    if sio:
        sio.disconnect()
        sio.wait()
