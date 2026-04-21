import os
import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError


os.environ['MONGO_URL'] = 'mongodb://localhost:27017'

@pytest.fixture
def dao_video():
    dao_video = DAO('video')
    yield dao_video
    dao_video.collection.drop()

@pytest.fixture
def dao_todo():
    dao_todo = DAO('todo')
    yield dao_todo
    dao_todo.collection.drop()


# Creates a video document with given url as input
    # Expects to get a object with _id
@pytest.mark.integration
def test_create_video_document_valid_id(dao_video):
    result = dao_video.create({'url': 'www.youtube.com//example1'})
    assert result['_id'] is not None

# Creates a video document with given url as input
    # Expects to get a object with url back
@pytest.mark.integration
def test_create_video_document_valid_url(dao_video):
    result = dao_video.create({'url': 'www.youtube.com//example1'})
    assert result['url'] == 'www.youtube.com//example1'

# Creates a video document with a unvalid url as input
    # Expects to get a writeError back
@pytest.mark.integration
def test_create_video_document_unvalid(dao_video):
    with pytest.raises(WriteError):
        dao_video.create({'url': 1234})


# Creates a todo document with description = "Vattna blommor" and done = True
    # Expects to get a object with _id
@pytest.mark.integration
def test_create_todo_document_valid_id(dao_todo):
    result = dao_todo.create({'description': 'Vattna blommor', 'done': True})
    assert result['_id'] is not None

# Creates a todo document with description = "Vattna blommor" and done = True
    # Expects to get a object with correct description
@pytest.mark.integration
def test_create_todo_document_valid_description(dao_todo):
    result = dao_todo.create({'description': 'Vattna blommor', 'done': True})
    assert result['description'] == 'Vattna blommor'

# Creates a todo document with description = "Vattna blommor" and done = True
    # Expects to get a object with done = True
@pytest.mark.integration
def test_create_todo_document_valid_bool(dao_todo):
    result = dao_todo.create({'description': 'Vattna blommor', 'done': True})
    assert result['done'] == True

# Creates a todo document with description = "Vattna blommor" and done = "Ja"
    # Expects to get a writeError back
@pytest.mark.integration
def test_create_todo_document_unvalid(dao_todo):
    with pytest.raises(WriteError):
        dao_todo.create({'description': 'Vattna blommor', 'done': 'Ja'})

# Creates two todo document with diffrent desctriptions
    # Expect to get last document back
@pytest.mark.integration
def test_create_two_documents_unique(dao_todo):
    dao_todo.create({'description': 'Vattna blommor', 'done': False})
    result = dao_todo.create({'description': 'Klipp gräset', 'done': True})    
    assert result['description'] == 'Klipp gräset'

# Creates two todo document with same description
    # Expect to get writeError due to unique identifier missused
@pytest.mark.integration
def test_create_two_documents_unique(dao_todo):
    dao_todo.create({'description': 'Vattna blommor', 'done': False})
    with pytest.raises(WriteError):
        dao_todo.create({'description': 'Vattna blommor', 'done': True})    
