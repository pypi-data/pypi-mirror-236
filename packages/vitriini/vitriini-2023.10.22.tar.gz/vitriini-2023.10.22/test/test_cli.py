import vitriini.cli as cli


def test_parser():
    assert cli.parser()


def test_app_valid():
    assert cli.app([]) == 0
