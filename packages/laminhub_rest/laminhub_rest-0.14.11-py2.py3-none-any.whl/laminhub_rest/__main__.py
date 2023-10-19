import argparse
import os
import sys
from subprocess import run
from typing import Literal, Optional

import sqlmodel as sqm
from lamin_logger import logger
from packaging.version import parse as vparse

from laminhub_rest._ci import start_local_supabase, supabase
from laminhub_rest.connector import Environment

# Grab environment variables to configure settings

LAMIN_ENV = os.environ.get("LAMIN_ENV")
if not LAMIN_ENV:
    os.environ["LAMIN_ENV"] = LAMIN_ENV = "local"
    logger.info("LAMIN_ENV not set, defaulting to 'local'")
elif LAMIN_ENV == "local":
    logger.info("lnhub running in local environment")
else:
    logger.warning(f"lnhub running in {LAMIN_ENV}!")
    confirmation = input("Do you want to proceed? (y/n)")
    if confirmation != "y":
        sys.exit(0)

# Functions


def run_supabase(args: argparse.Namespace, additional_args: list = []):
    if LAMIN_ENV == "local":
        if args.action == "stop":
            supabase(stop=True)
        elif args.action == "start":
            start_local_supabase()


def deploy(breaks_lndb: Optional[Literal["y", "n"]] = None):
    from lamindb_setup import settings

    from laminhub_rest.connector import get_engine
    from laminhub_rest.schema import __version__, _migration
    from laminhub_rest.schema.versions import version_cbwk

    if len(__version__.split(".")) != 3:
        raise RuntimeError("Your __version__ string is not of form X.X.X")

    if breaks_lndb is None:
        raise RuntimeError("Error: Pass --breaks-lndb y or --breaks-lndb n")

    if LAMIN_ENV == "local":
        raise RuntimeError(
            "Execute ./docs/00-migrate.ipynb to perform migration on local supabase."
        )

    if breaks_lndb:
        response = input(
            "Have you ensured that lndb and lamindb have releases on PyPI that users"
            " can pull?"
        )
        if response == "y":
            pass
        else:
            raise RuntimeError(
                "Please test thoroughly and prepare releases for lndb and lamindb.\n"
                "Pin laminhub_rest in lamindb, set a lower bound in lndb."
            )

    if settings.user.handle.startswith(("test", "static-test")):
        raise RuntimeError("Error: Log in with your developer handle, e.g., falexwolf")

    engine = get_engine()
    # check that a release was made
    with sqm.Session(engine) as ss:
        deployed_v = ss.exec(
            sqm.select(version_cbwk.v)
            .order_by(version_cbwk.v.desc())  # type: ignore
            .limit(1)
        ).one()
    if deployed_v == __version__:
        raise RuntimeError("Error: Make a new release before deploying the migration!")
    if vparse(deployed_v) > vparse(__version__):
        raise RuntimeError(
            "The new version has to be greater than the deployed version."
        )

    process = run(
        "alembic --config laminhub_rest/schema/alembic.ini --name cbwk upgrade head",
        shell=True,
    )
    if process.returncode == 0:
        with sqm.Session(engine) as ss:
            ss.add(
                version_cbwk(
                    v=__version__,
                    migration=_migration,
                    user_id=settings.user.id,
                    breaks_lndb=(breaks_lndb == "y"),
                )
            )
            ss.commit()

        logger.success("Successfully migrated hub.")


def run_server(args: argparse.Namespace, additional_args: list = []):
    run(
        ["python3", "./laminhub_rest/main.py"],
    )


def test(args: argparse.Namespace, additional_args: list = []):
    run_args = ["python3", "-m", "nox"] + additional_args
    run(
        run_args,
    )


def jupyter(args: argparse.Namespace, additional_args: list = []):
    run(
        "jupyter lab",
        shell=True,
    )


def ipython(args: argparse.Namespace, additional_args: list = []):
    if LAMIN_ENV == "local":
        start_local_supabase()
    from IPython import embed

    embed(colors="neutral")


def migrate(args: argparse.Namespace, additional_args: list = []):
    alembic_cmd = [
        "alembic",
        "--config",
        "laminhub_rest/schema/alembic.ini",
        "--name",
        "cbwk",
    ]
    if args.action == "deploy":
        deploy(breaks_lndb=args.breaks_lndb)
    elif args.action == "generate":
        run(alembic_cmd + ["revision", "--autogenerate", "-m", "vX.X.X."])
    else:
        run(alembic_cmd + [args.action] + additional_args)


# Parser handling

description_cli = "Manage hub."
parser = argparse.ArgumentParser(
    description=description_cli, formatter_class=argparse.RawTextHelpFormatter
)
subparsers = parser.add_subparsers(
    title="command", required=True, dest="subparser_name"
)
parser.add_argument(
    "-d", "--debug", dest="debug", action="store_true", help="Turn on debugging output"
)

# migrate
migration_parser = subparsers.add_parser("alembic", help="Manage migrations")
migration_parser.add_argument("action", help="Alembic action")
migration_parser.add_argument(
    "--breaks-lndb",
    choices=["y", "n"],
    default=None,
    help="Specify whether migration will break lndb (y/n).",
)
migration_parser.set_defaults(func=migrate)

# run
run_parser = subparsers.add_parser("run", help="Run FastAPI server")
run_parser.set_defaults(func=run_server)
# test
test_parser = subparsers.add_parser("test", help="Run nox tests")
test_parser.set_defaults(func=test)
# jupyter lab
jupyter_parser = subparsers.add_parser("jupyter", help="Launch Jupyter Notebook")
jupyter_parser.set_defaults(func=jupyter)
# ipython
ipython_parser = subparsers.add_parser("shell", help="Launch IPython terminal")
ipython_parser.set_defaults(func=ipython)
# supabase
supabase_parser = subparsers.add_parser("supabase", help="Run Supabase operations")
supabase_parser.add_argument(
    "action", choices=["start", "stop"], help="pass through to supabase CLI"
)
supabase_parser.set_defaults(func=run_supabase)


# parse args
def main():
    # Doing this allows us to pass arbitrary arguments to the subcommands
    args, additional_args = parser.parse_known_args()

    # Enable some easier debugging output
    if args.debug:
        logger.configure(
            handlers=[dict(sink=sys.stdout, format="{level.icon} {message}", level=10)]
        )
        logger.level("DEBUG", icon="🕵️")
    logger.debug(f"Args {args}")
    logger.debug(f"Additional args {additional_args}")
    if LAMIN_ENV == "local":
        logger.warning("Ensure local Supabase instance is up for LAMIN_ENV=local")
        # can't do the following right now because it doesn't work if several containers
        # are excluded (it fails on `supabase status`)
        # start_local_supabase()

    env = Environment()
    logger.debug(f"Environment: {env}")

    # Use the default functions per sub parser instead of writing
    # conditional logic
    args.func(args, additional_args=additional_args)
