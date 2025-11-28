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