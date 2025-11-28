from fastapi.testclient import TestClient

from tests.utils import api_routes
from tests.utils.fixture_schemas import TestUser


def test_get_token_success(api_client: TestClient, unique_user: TestUser):
    """
    Tests that a user can successfully log in with correct credentials and receive a token.
    """
    response = api_client.post(
        api_routes.auth_token,
        data={"username": unique_user.email, "password": unique_user.password},
    )

    assert response.status_code == 200
    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"
    assert "mealie.access_token" in response.cookies


def test_get_token_unknown_user(api_client: TestClient):
    """
    Tests that a login attempt with a non-existent username fails with a 401 Unauthorized error.
    """
    response = api_client.post(
        api_routes.auth_token,
        data={"username": "unknown@user.com", "password": "password"},
    )

    assert response.status_code == 401
    assert "mealie.access_token" not in response.cookies


def test_logout(api_client: TestClient, unique_user: TestUser):
    """
    Tests that the logout endpoint clears the access token cookie.
    """
    # First, ensure we are logged in
    login_response = api_client.post(
        api_routes.auth_token,
        data={"username": unique_user.email, "password": unique_user.password},
    )
    assert "mealie.access_token" in login_response.cookies
    token = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

    # Then, log out
    logout_response = api_client.post(api_routes.auth_logout, headers=token)

    assert logout_response.status_code == 200
    # The main purpose of logout is to delete the cookie, which is done via the 'set-cookie' header
    assert "set-cookie" in logout_response.headers
    set_cookie_header = logout_response.headers["set-cookie"]
    assert 'mealie.access_token=""' in set_cookie_header
    assert "Max-Age=0" in set_cookie_header

    # Verify a protected endpoint still works with the old token, since logout is client-side.
    refresh_response = api_client.get(api_routes.auth_refresh, headers=token)
    # The token itself is a self-contained JWT, it remains valid until it expires.
    # The logout just removes it from the client.
    # So a subsequent request *with the token* will still work.
    # The important part is that the cookie is gone from the client's perspective.
    assert refresh_response.status_code == 200
