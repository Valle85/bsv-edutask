import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_dao():
    return MagicMock()

@pytest.fixture
def controller(mock_dao):
    return UserController(mock_dao)

# Test case for existing user with valid email address
@pytest.mark.unit
def test_one_user(controller, mock_dao):
    mock_dao.find.return_value = [
        {"email": "test@test.com", "name": "Test User"}
    ]

    result = controller.get_user_by_email("test@test.com")

    assert result == {"email": "test@test.com", "name": "Test User"}


# Test case for invalid email address
@pytest.mark.unit
def test_invalid_email(controller):
    with pytest.raises(ValueError):
        controller.get_user_by_email("test.com")

# Test case for multiple users with the same email address
    # Return first username
@pytest.mark.unit
def test_multiple_users(controller, mock_dao):
    mock_dao.find.return_value = [
        {"email": "test@test.com", "name": "User1"},
        {"email": "test@test.com", "name": "User2"}
    ]

    result = controller.get_user_by_email("test@test.com")

    assert result == {"email": "test@test.com", "name": "User1"}

# Test case for multiple users with the same email address
    # Function prints warning when multiple users found
@pytest.mark.unit
def test_multiple_users_print(controller, mock_dao, capsys):
    mock_dao.find.return_value = [
        {"email": "test@test.com", "name": "User1"},
        {"email": "test@test.com", "name": "User2"}
    ]

    result = controller.get_user_by_email("test@test.com")
    captured = capsys.readouterr()

    assert "Error" in captured.out

# Test case for no user found with the given email address
# The test case for no user found fails due to an IndexError. 
# The function attempts to access the first element of an empty list 
# instead of returning None as specified.
@pytest.mark.unit
def test_no_user(controller, mock_dao):
    mock_dao.find.return_value = []
    result = controller.get_user_by_email("test@test.com")

    assert result is None

# Test case for database error during the search operation
@pytest.mark.unit
def test_db_fail(controller, mock_dao):
    mock_dao.find.side_effect = Exception()

    with pytest.raises(Exception):
        controller.get_user_by_email("test@test.com")
