# -*- coding: utf-8 -*-


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
