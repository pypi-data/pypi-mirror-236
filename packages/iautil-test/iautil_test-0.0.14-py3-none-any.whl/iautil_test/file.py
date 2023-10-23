""" mock file """

from unittest.mock import MagicMock
#from pathlib import Path
from io import TextIOBase
from typing import Callable
from typing import Union
from pytest import fixture#, MonkeyPatch
#from pytest_mock import MockerFixture

from iautil_test.strings import DEFAULT_CONTENT

class MockFile(TextIOBase):
    """ mock the open() function """

    def __init__(self, content:str):#, return_read:str):
        """ set the mock return values """
        TextIOBase.__init__(self)
        #MagicMock.__init__(self)
        self.content = content

    def read(self, size:Union[int,None]=-1)->str: # pylint: disable=unused-argument
        """ mock read() """
        return self.content

    def seekable(self)->bool:
        return False


#@fixture

def mock_file(
    content:str
)->Callable[[str,str],MagicMock]:
    """ mock file """
    def mock_open(file:str, mode:str='r')->MagicMock: # pylint: disable=unused-argument,redefined-outer-name
        """ mock open() """
        my_file:MockFile = MockFile(content)
        mock_obj:MagicMock = MagicMock(return_value=my_file)
        return mock_obj
    #mypatch.setattr("builtins.open", mock_open)
    return mock_open

@fixture
def mock_open(
)->Callable[[str,str],MagicMock]:
    """ mock_file() with default content """
    return mock_file(DEFAULT_CONTENT)

#@fixture
#def my_mock_file(
#):
#    """ mock_file with my content """
#    return mock_file("override content")

#@fixture
#def mock_open_return_read(
#    monkeypatch:MonkeyPatch, # pylint: disable=redefined-outer-name
#    #return_read:str=RETURN_READ_DEFAULT
#)->Callable[
#        [str,str],MockFile]:
#    """ mock open() """
#    #mock_file:MockFile = MockFile(return_read)
#    def my_mock_open(file: str, mode: str = 'r')->MockFile: # pylint: disable=unused-argument
#        """ MockFile with parameters """
#        return MockFile()#return_read)
#
#    monkeypatch.setattr("builtins.open", my_mock_open)
#    #monkeypatch.setattr("builtins.open", MagicMock(return_value=mock_file))
#    return my_mock_open

#@fixture
#def mock_open(
#    mock_open_return_read:Callable[[str,str],MockFile] # pylint: disable=redefined-outer-name
#)->Callable[
#        [str,str],MockFile]:
#    """ helper to use default values """
#    return mock_open_return_read
