#test for todo creation
def test_create_todo(client):

    # Login first to get token
    login = client.post(
        "/api/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    token = login.get_json()["token"]

    response = client.post(
        "/api/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Todo",
            "description": "Testing create endpoint",
            "priority": "high"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "Test Todo"
    assert data["priority"] == "high"

#test to get todos

def test_get_todos(client):

    login = client.post(
        "/api/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    token = login.get_json()["token"]

    response = client.get(
        "/api/todos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200