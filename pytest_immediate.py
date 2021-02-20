# The MIT License (MIT)
#
# Copyright (c) 2020-2021 Dominik Meier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import json
from typing import List

import pytest
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
        '--send-reports',
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


def setup_server():
    global sio
    uri = saved_config_options.remote_connection_address
    sio = socketio.Client()
    sio.connect(uri)


@pytest.hookimpl()
def pytest_runtest_logreport(report):
    if saved_config_options.send_reports:
        sio.emit("testreport", {"id": report.nodeid,
                                "when": report.when,
                                "outcome": report.passed})


# TODO this is ugly hardcoded, as well as should not be global.
#  The function might be fixed with currying
max_test_index = 100000
test_indexes = {}


def get_test_index(test):
    test_name = test.nodeid
    if test_name in test_indexes:
        return test_indexes[test_name]
    return max_test_index


@pytest.hookimpl()
def pytest_collection_modifyitems(session, config, items: List[Item]):
    global saved_config_options, sio
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

    sio = None
    if config.option.send_reports:
        setup_server()


@pytest.hookimpl()
def pytest_sessionfinish():
    if sio:
        sio.disconnect()
        sio.wait()
