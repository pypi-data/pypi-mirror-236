sql_rls_instance_account_db_user = """
    ALTER TABLE account_instance_db_user ENABLE ROW LEVEL SECURITY;

    CREATE POLICY "Enable a users to see their db users"
    ON public.account_instance_db_user
    FOR SELECT USING (
        account_id = auth.uid()
    );
    CREATE POLICY "Enable users to use db users"
    ON public.account_instance_db_user
    FOR INSERT
    WITH CHECK (
        account_id = auth.uid()
    );
    CREATE POLICY "Enable users to update their db users"
    ON public.account_instance_db_user
    FOR UPDATE USING (
        account_id = auth.uid()
    )
    WITH CHECK (
        account_id = auth.uid()
    );
    CREATE POLICY "Enable users to delete their db users"
    ON public.account_instance_db_user
    FOR DELETE USING (
        account_id = auth.uid()
    );
"""  # noqa

sql_drop_rls_laminapp_admin_instance = """
    DROP POLICY "Enable a users to see their db users" ON public.account_instance_db_user;
    DROP POLICY "Enable users to use db users" ON public.account_instance_db_user;
    DROP POLICY "Enable users to update their db users" ON public.account_instance_db_user;
    DROP POLICY "Enable users to delete their db users in cloud_run_instance table" ON public.account_instance_db_user;
"""  # noqa
