import logging

import pandas as pd
from typing_extensions import Literal

from typhoon_dbapi.hooks.dbapi_hooks import DbApiHook


def df_write(
        df: pd.DataFrame,
        hook: DbApiHook,
        table_name: str,
        schema: str = None,
        if_exists: Literal['fail', 'replace', 'append'] = 'append',
):
    """
    Given conn_id belonging to a SqlAlchemy hook, create or append the data to the specified table
    :param df: Dataframe with data
    :param hook: SqlAlchemyHook instance
    :param table_name: Name of the table to write to
    :param schema: Schema where the table is located
    :param if_exists: {'fail', 'replace', 'append'}, default 'append'
    :return:
    """
    with hook as conn:
        logging.info(f'Writing dataframe to {hook.conn_params.conn_type} table {table_name}, schema {schema or "default"}')
        df.to_sql(name=table_name, con=conn, schema=schema, if_exists=if_exists)
    return schema, table_name
