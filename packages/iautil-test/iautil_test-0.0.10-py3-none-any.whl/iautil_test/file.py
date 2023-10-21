""" mock file """

#from unittest.mock import MagicMock
#from pathlib import Path
from typing import Callable
from pytest import fixture, MonkeyPatch
#from pytest_mock import MockerFixture

RETURN_READ_DEFAULT:str = "Bonsoir, Elliot!"

class MockFile:#(MagicMock,File):
    """ mock the open() function """

    def __init__(self, return_read:str):
        """ set the mock return values """
        self.return_read = return_read

    def read(self)->str:
        """ mock read() """
        return self.return_read

    def __enter__(self):
        """ dummy enter """
        return self

    def __exit__(self, *args)->None:
        """ dummy exit """


@fixture
def mock_open_return_read(
    monkeypatch:MonkeyPatch, # pylint: disable=redefined-outer-name
    return_read:str=RETURN_READ_DEFAULT)->Callable[
        [str,str],MockFile]:
    """ mock open() """
    #mock_file:MockFile = MockFile(return_read)
    def my_mock_open(file: str, mode: str = 'r')->MockFile: # pylint: disable=unused-argument
        """ MockFile with parameters """
        return MockFile(return_read)

    monkeypatch.setattr("builtins.open", my_mock_open)
    #monkeypatch.setattr("builtins.open", MagicMock(return_value=mock_file))
    return my_mock_open

@fixture
def mock_open(
    mock_open_return_read:Callable[[str,str],MockFile] # pylint: disable=redefined-outer-name
)->Callable[
        [str,str],MockFile]:
    """ helper to use default values """
    return mock_open_return_read
