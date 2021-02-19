# -*- coding: utf-8 -*-
from unittest import mock


def test_reordering(testdir):
    testdir.makepyfile("""
        import pytest

        def test_one():
            print("One")

        def test_two():
            print("Two")
    """)

    result = testdir.runpytest(
        '-v',
        '--test-ordering=["test_reordering.py::test_one",'
        '"test_reordering.py::test_two"]',
    )

    result.stdout.fnmatch_lines([
        '*::test_one PASSED*',
        '*::test_two PASSED*',
    ])

    results_reordering = testdir.runpytest(
        '-v',
        '--test-ordering=["test_reordering.py::test_two",'
        '"test_reordering.py::test_one"]',
    )

    # Check if the order was switched
    results_reordering.stdout.fnmatch_lines([
        '*::test_two PASSED*',
        '*::test_one PASSED*',
    ])


def test_socket_send(testdir):
    with mock.patch("socketio.Client") as mock_class:
        testdir.makepyfile("""
            import pytest

            def test_one():
                print("One")

            def test_two():
                print("Two")
        """)

        testdir.runpytest()
        assert mock_class.mock_calls == []

        testdir.runpytest(
            '--send-reports'
        )
        assert mock_class.mock_calls == [
            mock.call(),
            mock.call().connect('ws://localhost:9001'),
            mock.call().emit('testreport', {'id': 'test_socket_send.py::test_one', 'when': 'setup', 'outcome': True}),
            mock.call().emit('testreport', {'id': 'test_socket_send.py::test_one', 'when': 'call', 'outcome': True}),
            mock.call().emit('testreport', {'id': 'test_socket_send.py::test_one', 'when': 'teardown', 'outcome': True}),
            mock.call().emit('testreport', {'id': 'test_socket_send.py::test_two', 'when': 'setup', 'outcome': True}),
            mock.call().emit('testreport', {'id': 'test_socket_send.py::test_two', 'when': 'call', 'outcome': True}),
            mock.call().emit('testreport', {'id': 'test_socket_send.py::test_two', 'when': 'teardown', 'outcome': True}),
            mock.call().__bool__(),
            mock.call().disconnect(),
            mock.call().wait(),
        ]
