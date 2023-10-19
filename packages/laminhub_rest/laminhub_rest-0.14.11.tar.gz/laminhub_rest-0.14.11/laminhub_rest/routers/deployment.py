import os
from typing import Literal, Union
from uuid import uuid4

import requests  # type: ignore
from fastapi import APIRouter, Header
from lamin_logger import logger

from laminhub_rest.core.instance._get_account_role_for_instance import (
    get_account_role_for_instance,
)
from laminhub_rest.orm._cloud_run_instance import sb_insert_cloud_run_instance
from laminhub_rest.orm._instance import select_instance_by_owner_name
from laminhub_rest.routers.utils import extract_access_token
from laminhub_rest.utils._supabase_client import SbClientAdmin, SbClientFromAccesToken

router = APIRouter(prefix="/deploy")


@router.post("/{owner_handle}/{instance_name}")
def deploy(
    owner_handle: str,
    instance_name: str,
    env: Literal["hp", "hpt", "hs", "hst"] = "hp",
    cloud_run_instance_name_prefix: str = "",
    authentication: Union[str, None] = Header(default=None),
):
    instance_identifier = f"{owner_handle}/{instance_name}"
    owner = "laminlabs"
    repo = "laminapp-rest"
    github_token = os.environ["GH_ACCESS_TOKEN"]

    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        instance = select_instance_by_owner_name(
            owner_handle, instance_name, supabase_client
        )

    if instance is None:
        error_message = "Instance not found."
        logger.error(error_message)
        return {"status": "error", "message": error_message}

    role = get_account_role_for_instance(
        access_token=access_token,
        instance_id=instance["id"],
        supabase_client=supabase_client,
    )

    if role != "admin":
        error_message = (
            "Only instance admin can perform laminapp-rest server deployment."
        )
        logger.error(error_message)
        return {"status": "error", "message": error_message}

    with SbClientAdmin().connect() as supabase_client_admin:
        sb_insert_cloud_run_instance(uuid4().hex, instance["id"], supabase_client_admin)

    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    headers = {
        "Accept": "application/vnd.github.everest-preview+json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}",
    }
    payload = {
        "event_type": f"deploy-lamin-instance-{env}",
        "client_payload": {
            "LAMIN_INSTANCE_IDENTIFIER": instance_identifier,
            "CLOUD_RUN_INSTANCE_NAME_PREFIX": cloud_run_instance_name_prefix,
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 204:
        logger.info("Workflow dispatched successfully.")
        return {"status": "success", "message": "Workflow dispatched successfully."}
    else:
        error_message = (
            f"Failed to dispatch workflow. Response: {response.status_code} -"
            f" {response.text}"
        )
        logger.error(error_message)
        return {"status": "error", "message": error_message}
