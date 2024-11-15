import pytest
from main import app, db, Task

@pytest.fixture
def client():
    # Configure Flask testing environment
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_create_task(client):
    response = client.post('/tasks', json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 201
    data = response.get_json()
    assert data['task']['title'] == "Test Task"

def test_get_tasks(client):
    client.post('/tasks', json={"title": "Task 1", "description": "Description 1"})
    client.post('/tasks', json={"title": "Task 2", "description": "Description 2"})
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 2

def test_update_task(client):
    response = client.post('/tasks', json={"title": "Old Title", "description": "Old Description"})
    task_id = response.get_json()['task']['id']
    update_response = client.put(f'/tasks/{task_id}', json={"title": "New Title", "done": True})
    assert update_response.status_code == 200
    updated_data = update_response.get_json()['task']
    assert updated_data['title'] == "New Title"
    assert updated_data['done'] is True

def test_delete_task(client):
    response = client.post('/tasks', json={"title": "Task to Delete"})
    task_id = response.get_json()['task']['id']
    delete_response = client.delete(f'/tasks/{task_id}')
    assert delete_response.status_code == 200
