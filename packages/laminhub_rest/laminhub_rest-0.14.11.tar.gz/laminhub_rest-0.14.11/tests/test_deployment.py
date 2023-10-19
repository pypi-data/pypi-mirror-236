from unittest.mock import Mock, patch

from laminhub_rest.main import client as test_client


# Success Test
@patch("laminhub_rest.routers.deployment.os")
@patch("laminhub_rest.routers.deployment.requests.post")
@patch("laminhub_rest.routers.deployment.SbClientAdmin")
@patch("laminhub_rest.routers.deployment.SbClientFromAccesToken")
@patch("laminhub_rest.routers.deployment.extract_access_token")
@patch("laminhub_rest.routers.deployment.get_account_role_for_instance")
def test_deploy_success(
    mock_get_account_role_for_instance,
    mock_extract_access_token,
    mock_sb_client_from_token,
    mock_sb_client_admin,
    mock_post,
    mock_os,
):
    # Setup
    mock_os.environ = {"GH_ACCESS_TOKEN": "fake_token"}
    mock_post.return_value.status_code = 204
    mock_extract_access_token.return_value = "mock_access_token"
    mock_get_account_role_for_instance.return_value = "admin"
    mock_instance = {"id": "mock_instance_id"}

    mock_execute_return = Mock(data=[mock_instance])
    mock_client = mock_sb_client_from_token().connect().__enter__.return_value
    mock_client.table().select().eq().eq().execute.return_value = mock_execute_return

    mock_sb_client_admin().connect().__enter__.return_value.sb_insert_cloud_run_instance.return_value = (  # noqa
        None
    )

    # Test
    response = test_client.post(
        "/deploy/owner1/instance1", headers={"authentication": "mock_auth"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Workflow dispatched successfully.",
    }


@patch("laminhub_rest.routers.deployment.os")
@patch("laminhub_rest.routers.deployment.SbClientFromAccesToken")
@patch("laminhub_rest.routers.deployment.extract_access_token")
def test_deploy_instance_none(
    mock_extract_access_token,
    mock_sb_client_from_token,
    mock_os,
):
    # Setup
    mock_os.environ = {"GH_ACCESS_TOKEN": "fake_token"}
    mock_extract_access_token.return_value = "mock_access_token"
    mock_execute_return = Mock(data=[])

    mock_client = mock_sb_client_from_token().connect().__enter__.return_value
    mock_client.table().select().eq().eq().execute.return_value = mock_execute_return

    # Test
    response = test_client.post(
        "/deploy/owner1/instance1", headers={"authentication": "mock_auth"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Instance not found.",
    }


@patch("laminhub_rest.routers.deployment.os")
@patch("laminhub_rest.routers.deployment.SbClientFromAccesToken")
@patch("laminhub_rest.routers.deployment.extract_access_token")
@patch("laminhub_rest.routers.deployment.get_account_role_for_instance")
def test_deploy_not_admin(
    mock_get_account_role_for_instance,
    mock_extract_access_token,
    mock_sb_client_from_token,
    mock_os,
):
    # Setup
    mock_os.environ = {"GH_ACCESS_TOKEN": "fake_token"}
    mock_extract_access_token.return_value = "mock_access_token"
    mock_get_account_role_for_instance.return_value = "read"
    mock_instance = {"id": "mock_instance_id"}

    mock_execute_return = Mock(data=[mock_instance])
    mock_client = mock_sb_client_from_token().connect().__enter__.return_value
    mock_client.table().select().eq().eq().execute.return_value = mock_execute_return

    # Test
    response = test_client.post(
        "/deploy/owner1/instance1", headers={"authentication": "mock_auth"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Only instance admin can perform laminapp-rest server deployment.",
    }


@patch("laminhub_rest.routers.deployment.os")
@patch("laminhub_rest.routers.deployment.requests.post")
@patch("laminhub_rest.routers.deployment.SbClientAdmin")
@patch("laminhub_rest.routers.deployment.SbClientFromAccesToken")
@patch("laminhub_rest.routers.deployment.extract_access_token")
@patch("laminhub_rest.routers.deployment.get_account_role_for_instance")
def test_deploy_github_workflow_failure(
    mock_get_account_role_for_instance,
    mock_extract_access_token,
    mock_sb_client_from_token,
    mock_sb_client_admin,
    mock_post,
    mock_os,
):
    # Setup
    mock_os.environ = {"GH_ACCESS_TOKEN": "fake_token"}
    mock_post.return_value.status_code = 400  # Change to a failure status code
    mock_post.return_value.text = "Bad Request"
    mock_extract_access_token.return_value = "mock_access_token"
    mock_get_account_role_for_instance.return_value = "admin"
    mock_instance = {"id": "mock_instance_id"}

    mock_execute_return = Mock(data=[mock_instance])
    mock_client = mock_sb_client_from_token().connect().__enter__.return_value
    mock_client.table().select().eq().eq().execute.return_value = mock_execute_return

    mock_sb_client_admin().connect().__enter__.return_value.sb_insert_cloud_run_instance.return_value = (  # noqa
        None
    )

    # Test
    response = test_client.post(
        "/deploy/owner1/instance1", headers={"authentication": "mock_auth"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Failed to dispatch workflow. Response: 400 - Bad Request",
    }
