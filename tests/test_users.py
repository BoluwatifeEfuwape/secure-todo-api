import uuid

# Test user registration
def test_register_user(client):

    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    unique_email = f"test_{uuid.uuid4()}@example.com"

    response = client.post(
        "/api/users/register",
        json={
            "username": unique_username,
            "email": unique_email,
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    

    # print(response.status_code)
    # print(response.get_json())

    assert "token" in data
    assert data["user"]["email"] == unique_email


# Test login
def test_login_user(client):

    unique_email = f"login_{uuid.uuid4()}@example.com"
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    # Register user first
    client.post(
        "/api/users/register",
        json={
            "username": unique_username,
            "email": unique_email,
            "password": "password123"
        }
    )

    # Now login
    response = client.post(
        "/api/users/login",
        json={
            "email": unique_email,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "token" in data
    assert data["message"] == "Login successful"