from lamin_vault.server._get_vault_client_approle import get_vault_approle_client


def test_get_vault_approle_client():
    client = get_vault_approle_client()
    assert client is not None, "Client should not be None"
    assert client.is_authenticated(), "Client should be authenticated"


# def test_create_token_from_jwt(test_client, hub_rest_api_url, user_account_for_vault):
#     auth, account = user_account_for_vault
#     response = test_client.post(
#         f"{hub_rest_api_url}/vault/token/from-jwt/{instance_id}",
#         headers={"authentication": f"Bearer {auth['access_token']}"},
#     )
#     assert response.status_code == 200
#     assert response.json() is not None


# def test_create_instance_admin_token_from_jwt(test_client):
#    response = test_client.post(
#        f"/vault/token/from-jwt/admin/{test_instance_id}",
#        headers={"authentication": "Bearer test_token"}
#    )
#    assert response.status_code == 200
#    assert response.json() is not None
