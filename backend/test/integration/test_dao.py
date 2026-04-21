
# Create Method
# Belongs to class DAO

# Method creates a new document in the collection associated to this data access object.
# Test  should cover the following.

# Test
    # DAO.create with all required fields -> should succed
# Test
    # DAO.create with one field wrong -> should fail with writeError
# Test
    # DAO.create with correct BSON data -> should succed
# Test
    # DAO.create with wrong BSON data -> should fail with writeError
# Test
    # DAO.create with boolean property -> should succed
# Test
    # DAO.create with wrong boolean property -> should fail with writeError
# Test
    # DAO.create two documents with diffrent values for unique identifiers -> should succed
# Test 
    # DAO.create two documents with same values for unique fields -> should fail with writeError
        # (This test fails probably faulth in code)

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
    # Expects to get a object with _id and url back
@pytest.mark.integration
def test_create_video_document_valid(dao_video):
    result = dao_video.create({'url': 'www.youtube.com//example1'})
    assert result['_id'] is not None and result['url'] == 'www.youtube.com//example1'

# Creates a video document with a unvalid url as input
    # Expects to get a writeError back
@pytest.mark.integration
def test_create_video_document_unvalid(dao_video):
    with pytest.raises(WriteError):
        dao_video.create({'url': 1234})


# Creates a todo document with description = "Vattna blommor" and done = True
    # Expects to get a object with _id, correct description and done = True
@pytest.mark.integration
def test_create_todo_document_valid(dao_todo):
    result = dao_todo.create({'description': 'Vattna blommor', 'done': True})
    assert result['_id'] is not None and result['description'] == 'Vattna blommor' and result['done'] == True

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
    assert result['_id'] is not None and result['description'] == 'Klipp gräset' and result['done'] == True

# Creates two todo document with same description
    # Expect to get writeError due to unique identifier missused
@pytest.mark.integration
def test_create_two_documents_unique(dao_todo):
    dao_todo.create({'description': 'Vattna blommor', 'done': False})
    with pytest.raises(WriteError):
        dao_todo.create({'description': 'Vattna blommor', 'done': True})    
