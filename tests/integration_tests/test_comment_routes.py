from fastapi.testclient import TestClient
from mealie.schema.recipe import Recipe
from tests.utils import api_routes
from tests.utils.factories import random_string
from tests.utils.fixture_schemas import TestUser


def test_create_comment(api_client: TestClient, random_recipe: Recipe, unique_user: TestUser):
    """
    Tests that a user can create a comment on a recipe.
    """
    comment_text = random_string()
    payload = {"recipe_id": str(random_recipe.id), "text": comment_text}
    response = api_client.post(api_routes.comments, json=payload, headers=unique_user.token)

    assert response.status_code == 201
    data = response.json()
    assert data["text"] == comment_text
    assert data["user"]["id"] == str(unique_user.user_id)
    assert data["recipeId"] == str(random_recipe.id)


def test_get_recipe_comments(api_client: TestClient, random_recipe: Recipe, unique_user: TestUser):
    """
    Tests that comments for a specific recipe can be retrieved.
    """
    # First, create a comment
    comment_text = random_string()
    payload = {"recipe_id": str(random_recipe.id), "text": comment_text}
    response = api_client.post(api_routes.comments, json=payload, headers=unique_user.token)
    assert response.status_code == 201
    comment_id = response.json()["id"]

    # Then, get comments for the recipe
    response = api_client.get(api_routes.recipes_slug_comments(random_recipe.slug), headers=unique_user.token)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Find the comment we created
    assert any(comment["id"] == comment_id and comment["text"] == comment_text for comment in data)


def test_update_own_comment(api_client: TestClient, random_recipe: Recipe, unique_user: TestUser):
    """
    Tests that a user can update their own comment.
    """
    # Create a comment
    comment_text = random_string()
    payload = {"recipe_id": str(random_recipe.id), "text": comment_text}
    response = api_client.post(api_routes.comments, json=payload, headers=unique_user.token)
    assert response.status_code == 201
    comment_id = response.json()["id"]

    # Update the comment
    updated_text = random_string()
    update_payload = {"id": comment_id, "text": updated_text}
    response = api_client.put(api_routes.comments_item_id(comment_id), json=update_payload, headers=unique_user.token)

    assert response.status_code == 200
    assert response.json()["text"] == updated_text


def test_admin_can_update_other_user_comment(
    api_client: TestClient, random_recipe: Recipe, unique_user: TestUser, unique_admin: TestUser
):
    """
    Tests that an admin user can update another user's comment.
    """
    # Create a comment as a normal user
    comment_text = random_string()
    payload = {"recipe_id": str(random_recipe.id), "text": comment_text}
    response = api_client.post(api_routes.comments, json=payload, headers=unique_user.token)
    assert response.status_code == 201
    comment_id = response.json()["id"]

    # Attempt to update as an admin
    updated_text = random_string()
    update_payload = {"id": comment_id, "text": updated_text}
    response = api_client.put(api_routes.comments_item_id(comment_id), json=update_payload, headers=unique_admin.token)

    assert response.status_code == 200
    assert response.json()["text"] == updated_text


def test_delete_own_comment(api_client: TestClient, random_recipe: Recipe, unique_user: TestUser):
    """
    Tests that a user can delete their own comment.
    """
    # Create a comment
    comment_text = random_string()
    payload = {"recipe_id": str(random_recipe.id), "text": comment_text}
    response = api_client.post(api_routes.comments, json=payload, headers=unique_user.token)
    assert response.status_code == 201
    comment_id = response.json()["id"]

    # Delete the comment
    response = api_client.delete(api_routes.comments_item_id(comment_id), headers=unique_user.token)
    assert response.status_code == 200

    # Verify it's gone
    response = api_client.get(api_routes.comments_item_id(comment_id), headers=unique_user.token)
    assert response.status_code == 404


def test_admin_can_delete_other_user_comment(
    api_client: TestClient, random_recipe: Recipe, unique_user: TestUser, unique_admin: TestUser
):
    """
    Tests that an admin user can delete another user's comment.
    """
    # Create a comment as a normal user
    comment_text = random_string()
    payload = {"recipe_id": str(random_recipe.id), "text": comment_text}
    response = api_client.post(api_routes.comments, json=payload, headers=unique_user.token)
    assert response.status_code == 201
    comment_id = response.json()["id"]

    # Attempt to delete as an admin
    response = api_client.delete(api_routes.comments_item_id(comment_id), headers=unique_admin.token)
    assert response.status_code == 200
