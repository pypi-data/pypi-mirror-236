import os

import nox
from laminci.nox import run_pre_commit

nox.options.default_venv_backend = "none"

COVERAGE_ARGS = "--cov=laminhub_rest --cov-append --cov-report=term-missing"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


def get_env_for_pytest():
    if os.environ["LAMIN_ENV"] == "local":
        return {
            "LAMIN_ENV": os.environ["LAMIN_ENV"],
            "VAULT_SERVER_URL": os.environ["VAULT_SERVER_URL"],
            "VAULT_ROLE_ID": os.environ["VAULT_ROLE_ID"],
            "VAULT_SECRET_ID": os.environ["VAULT_SECRET_ID"],
        }
    else:
        return {
            "LAMIN_ENV": os.environ["LAMIN_ENV"],
            "SUPABASE_API_URL": os.environ["SUPABASE_API_URL"],
            "SUPABASE_ANON_KEY": os.environ["SUPABASE_ANON_KEY"],
            "SUPABASE_SERVICE_ROLE_KEY": os.environ["SUPABASE_SERVICE_ROLE_KEY"],
            "LAMIN_HUB_REST_SERVER_URL": os.environ["LAMIN_HUB_REST_SERVER_URL"],
            "LNHUB_PG_PASSWORD": os.environ["LNHUB_PG_PASSWORD"],
            "POSTGRES_DSN": os.environ["POSTGRES_DSN"],
            "VAULT_SERVER_URL": os.environ["VAULT_SERVER_URL"],
            "VAULT_ROLE_ID": os.environ["VAULT_ROLE_ID"],
            "VAULT_SECRET_ID": os.environ["VAULT_SECRET_ID"],
        }


@nox.session
def test(session: nox.Session):
    session.run(*"pip install -e .[dev]".split())
    # the -n 1 is to ensure that supabase thread exits properly
    session.run(
        *f"pytest -n 1 {COVERAGE_ARGS}".split(),
        env=get_env_for_pytest(),
    )
