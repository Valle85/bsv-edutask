import os
import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError

os.environ['MONGO_URL'] = 'mongodb://localhost:27017'

@pytest.fixture
def dao_todo():
    dao_todo = DAO('todo')
    yield dao_todo
    dao_todo.collection.drop()

# Creates a todo document with description = "Vattna blommor" and done = True
    # Expects to get a object with _id
@pytest.mark.integration
def test_create_todo_document_valid(dao_todo):
    result = dao_todo.create({'description': 'Vattna blommor', 'done': True})
    assert result['_id'] is not None

# Creates two todo document with same description
    # Expect to get writeError due to unique identifier missused
@pytest.mark.integration
def test_create_two_documents_unique(dao_todo):
    dao_todo.create({'description': 'Vattna blommor', 'done': False})
    with pytest.raises(WriteError):
        dao_todo.create({'description': 'Vattna blommor', 'done': True})

# Creates a todo document with description = "Vattna blommor" and done = "Ja"
    # Expects to get a writeError back
@pytest.mark.integration
def test_create_todo_document_unvalid(dao_todo):
    with pytest.raises(WriteError):
        dao_todo.create({'description': 'Vattna blommor', 'done': 'Ja'})

# Creates a todo document withoit the required description field
    # Expects to get a writeError back
@pytest.mark.integration
def test_create_todo_document_missing_field(dao_todo):
    with pytest.raises(WriteError):
        dao_todo.create({'done': True})
