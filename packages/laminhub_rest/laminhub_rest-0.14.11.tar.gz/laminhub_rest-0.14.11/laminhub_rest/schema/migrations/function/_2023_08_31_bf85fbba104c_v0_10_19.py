sql_function_is_laminapp_admin = """
    CREATE OR REPLACE FUNCTION is_laminapp_admin(_account_id uuid) RETURNS boolean
       LANGUAGE plpgsql
       SECURITY DEFINER SET search_path = public
    AS
    $$BEGIN
       RETURN _account_id = '30ec40be-c1aa-4df3-935b-cad7891caffd';
    END;$$;
"""  # noqa
