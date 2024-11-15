import pytest
from main import app, db, Task

# Use Flask's test client
@pytest.fixture
def client():
    # Set the app's testing configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://adi:admin@mysql-service:3306/admin'  # Use an in-memory SQLite database for tests
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    db.session.remove()  # Clean up the session after tests


# Test POST /tasks endpoint without hitting the real database
def test_create_task(client, mocker):
    # Mock the db session methods to avoid hitting the actual database
    mock_add = mocker.patch('app.db.session.add')
    mock_commit = mocker.patch('app.db.session.commit')

    task_data = {'title': 'Test Task', 'description': 'Test description'}
    response = client.post('/tasks', json=task_data)

    # Check that the mock methods were called
    mock_add.assert_called_once()
    mock_commit.assert_called_once()

    # Check the response
    assert response.status_code == 201
    assert response.json['message'] == 'Task created'
    assert response.json['task']['title'] == 'Test Task'
    assert response.json['task']['description'] == 'Test description'


# Test GET /tasks endpoint without hitting the real database
def test_get_tasks(client, mocker):
    # Mock the database query
    mock_query_all = mocker.patch('app.Task.query.all', return_value=[
        Task(id=1, title='Test Task 1', description='Test description 1', done=False),
        Task(id=2, title='Test Task 2', description='Test description 2', done=True)
    ])

    response = client.get('/tasks')

    # Check that the mock method was called
    mock_query_all.assert_called_once()

    # Check the response
    assert response.status_code == 200
    assert len(response.json['tasks']) == 2
    assert response.json['tasks'][0]['title'] == 'Test Task 1'
    assert response.json['tasks'][1]['done'] is True
