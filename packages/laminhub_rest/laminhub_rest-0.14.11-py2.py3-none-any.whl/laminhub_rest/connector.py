# see the overlap with _hub_client.py in lamindb-setup

import os
from typing import Optional
from urllib.request import urlretrieve

from pydantic import BaseSettings, PostgresDsn
from sqlalchemy.future import Engine
from sqlmodel import create_engine
from supabase.lib.client_options import ClientOptions

from supabase import create_client

engine: Optional[Engine] = None


class Connector(BaseSettings):
    url: str
    key: str


def load_connector() -> Connector:
    if os.getenv("LAMIN_ENV") == "staging":
        url = "https://lamin-site-assets.s3.amazonaws.com/connector_staging.env"
    else:
        url = "https://lamin-site-assets.s3.amazonaws.com/connector.env"
    connector_file, _ = urlretrieve(url)
    connector = Connector(_env_file=connector_file)
    return connector


class Environment:
    def __init__(self):
        lamin_env = os.getenv("LAMIN_ENV")
        if lamin_env is None:
            lamin_env = "prod"
        if lamin_env in {"prod", "staging"}:
            connector = load_connector()
            supabase_api_url = connector.url
            supabase_anon_key = connector.key
        else:
            supabase_api_url = os.environ["SUPABASE_API_URL"]
            supabase_anon_key = os.environ["SUPABASE_ANON_KEY"]

        # used client side in lamindb-setup
        self.lamin_env: str = lamin_env
        self.supabase_api_url: str = supabase_api_url
        self.supabase_anon_key: str = supabase_anon_key

        # only used admin-side and in laminapp-rest
        self.postgres_dsn: Optional[PostgresDsn] = os.getenv("POSTGRES_DSN")
        self.supabase_service_role_key: Optional[str] = os.getenv(
            "SUPABASE_SERVICE_ROLE_KEY"
        )


def get_engine() -> Engine:
    global engine
    if engine is None:
        env = Environment()
        if env.postgres_dsn is not None:
            engine = create_engine(env.postgres_dsn, echo=True)
        else:
            engine = None
    return engine


def connect_hub(client_options: ClientOptions = ClientOptions()):
    env = Environment()

    return create_client(env.supabase_api_url, env.supabase_anon_key, client_options)


def connect_hub_with_auth(
    *,
    email: Optional[str] = None,
    password: Optional[str] = None,
    access_token: Optional[str] = None
):
    hub = connect_hub()
    if access_token is None:
        if email is None or password is None:
            from lamindb_setup import settings

            email = settings.user.email
            password = settings.user.password
        access_token = get_access_token(email=email, password=password)
    hub.postgrest.auth(access_token)
    return hub


def connect_hub_with_service_role():
    env = Environment()
    return create_client(env.supabase_api_url, env.supabase_service_role_key)


def get_access_token(email: Optional[str] = None, password: Optional[str] = None):
    hub = connect_hub()
    try:
        auth_response = hub.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
        return auth_response.session.access_token
    finally:
        hub.auth.sign_out()
