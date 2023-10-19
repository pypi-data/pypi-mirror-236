# Migrations

1. Create a new branch, bumping the version number.
2. Modify the schema by rewriting the ORMs (add a column, rename a column, add constraints, drop constraints, add an ORM, etc.)
3. Select the database against which to generate a migration script by setting the `LAMIN_ENV` and `POSTGRES_DSN` environment variables.

   - `LAMIN_ENV`: `local`, `staging`, or `prod`
   - `POSTGRES_DSN`: the DSN for the database of interest

4. Generate the migration script: `lnhub alembic generate`
5. Review the migration script in `laminhub_rest/schema/migrations/versions/` and update/extend it as needed, especially for RLS modifications.
6. Update the migration revision in `laminhub_rest/schema/__init__.py` to match that of the newly-created migration script.
7. Push the new branch to the remote `laminhub-rest` repo and create a PR into main.
8. Make sure the [hub tests against the local supabase instance](https://github.com/laminlabs/laminhub-rest/blob/9f3fbde7efa8adb7f3bdfaba59f5fbab498d07b0/noxfile.py#L16-L45) pass.
   - These tests spin up a fresh local supabase instance, migrate it based on the new migration script, and run the tests against it.
   - If tests fail, this means that either the migration is faulty or business logic must be updated to conform to the new database state.
9. Verify if the changes break the lamindb-setup client by checking [lamindb-setup tests against the local supabase instance](https://github.com/laminlabs/laminhub-rest/blob/9f3fbde7efa8adb7f3bdfaba59f5fbab498d07b0/noxfile.py#L48-L103).
   - If changes are breaking, pass `--breaks-lndb=y` to `lnhub alembic deploy` in the next step.
10. Once local tests pass, migrate the staging database.

- Make sure your `laminhub-rest` installation matches the version of the current branch (make a local installation of `laminhub_rest`).
- Make sure the `LAMIN_ENV` and `POSTGRES_DSN` environment variable are set to the correct target database.
- Run `lnhub alembic deploy` with the `--breaks-lndb` flag set accordingly.

11. Re-run the CI workflow to make sure that all tests against staging also pass.
12. Once staging tests pass, migrate the production database by following step 9, but with variables relevant to the production database.
13. Merge the PR into main, make a release commit (update the changelog), publish the release to PyPi via `flit publish`, and publish the release in GitHub.
