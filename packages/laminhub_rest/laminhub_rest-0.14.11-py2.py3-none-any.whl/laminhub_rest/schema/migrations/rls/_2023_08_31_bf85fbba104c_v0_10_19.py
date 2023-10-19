sql_rls_laminapp_admin_instance = """
    CREATE POLICY "Enable laminapp admin to select any instances"
    ON public.instance
    FOR SELECT USING (
        is_laminapp_admin(auth.uid())
    );

    CREATE POLICY "Enable laminapp admin to select any collaborators"
    ON public.account_instance
    FOR SELECT USING (
        is_laminapp_admin(auth.uid())
    );

    CREATE POLICY "Enable laminapp admin to select any db_user"
    ON public.db_user
    FOR SELECT USING (
        is_laminapp_admin(auth.uid())
    );

    CREATE POLICY "Enable laminapp admin to select any entry in cloud_run_instance table"
    ON public.cloud_run_instance
    FOR SELECT USING (
        is_laminapp_admin(auth.uid())
    );
"""  # noqa

sql_drop_rls_laminapp_admin_instance = """
    DROP POLICY "Enable laminapp admin to select any instances" ON public.instance;
    DROP POLICY "Enable laminapp admin to select any collaborators" ON public.account_instance;
    DROP POLICY "Enable laminapp admin to select any db_user" ON public.db_user;
    DROP POLICY "Enable laminapp admin to select any entry in cloud_run_instance table" ON public.cloud_run_instance;
"""  # noqa
