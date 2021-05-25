import logging
from contextlib import closing
from io import BytesIO, StringIO
from typing import Optional, NamedTuple, Sequence, Generator, Iterable, Union

import sqlparse

from typhoon_dbapi.hooks.dbapi_hooks import DbApiHook
from typhoon_dbapi.hooks.sqlalchemy_hook import SqlAlchemyHook


class ExecuteQueryResult(NamedTuple):
    metadata: dict
    columns: Sequence
    batch: Sequence[Sequence]


def execute_query(
        hook: DbApiHook,
        query: str,
        batch_size: Optional[int] = None,
        metadata: Optional[dict] = None,
        query_params: Optional[dict] = None,
        multi_query: bool = False,
        file_stream: Union[bytes, str, BytesIO, StringIO, None] = None,
) -> Generator[ExecuteQueryResult, None, None]:
    """
    Executes query against a relational database. Schema and table name are returned with the result since they can be
    useful for governance purposes.
    :param hook: DbApiHook instance
    :param schema:  Can be used as template parameter {{ schema }} inside the query
    :param table_name: Can be used as template parameter {{ table }} inside the query
    :param query: Query. Can be a jinja2 template
    :param batch_size: Used as parameter to fetchmany. Full extraction if not defined.
    :param query_params: Will used to render the query template
    :param file_stream: When executing a Snowflake PUT command, you can use this parameter to upload an in-memory file-like object (e.g. the I/O object returned from the Python open() function), rather than a file on the filesystem.
    :return: ExecuteQueryResult namedtuple
    """
    kwargs = {}
    if isinstance(file_stream, bytes):
        file_stream = BytesIO(file_stream)
    elif isinstance(file_stream, str):
        file_stream = StringIO(file_stream)
    if file_stream:
        kwargs['file_stream'] = file_stream
    with hook as conn:
        print(sqlparse.split(query))
        for single_query in (sqlparse.split(query) if multi_query else [query]):
            logging.info(f'Executing query: {single_query}')
            if isinstance(hook, SqlAlchemyHook):
                cursor = conn.engine.execute(single_query, query_params, **kwargs)
                columns = [x[0] for x in cursor._cursor_description()]
            else:
                cursor = conn.cursor()
                cursor.execute(single_query, query_params or [], **kwargs)
                columns = [x[0] for x in cursor.description] if cursor.description else None
            
            # @todo put connection to autocommit=True
            #conn.commit()

        if not batch_size:
            logging.info(f'Fetching all results')
            yield ExecuteQueryResult(
                metadata=metadata,
                columns=columns,
                batch=cursor.fetchall(),
            )
        else:
            while True:
                logging.info(f'Fetching {batch_size} rows')
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield ExecuteQueryResult(
                    metadata=metadata,
                    columns=columns,
                    batch=batch,
                )


def read_sql(hook: DbApiHook, query: str, batch_size: Optional[int] = None, metadata: dict = None):
    import pandas as pd
    with hook as conn:
        if batch_size is None:
            return pd.read_sql(query, conn), metadata
        for chunk in pd.read_sql(query, conn, chunksize=batch_size):
            yield chunk, metadata


def execute_many(hook: DbApiHook, query: str, seq_of_params: Iterable[tuple], metadata: dict = None) -> dict:
    with hook as conn, closing(conn.cursor()) as cursor:
        cursor.executemany(query, seq_of_params)
    return metadata


# def df_write(df: DataFrame, hook: SqlAlchemyHook, table_name: str, schema: str = None):
#     """
#     Given conn_id belonging to a SqlAlchemy hook, create or append the data to the specified table
#     :param df: Dataframe with data
#     :param hook: SqlAlchemyHook instance
#     :param table_name: Name of the table to write to
#     :param schema: Schema where the table is located
#     :return:
#     """
#     with hook as engine:
#         logging.info(f'Writing dataframe to {hook.conn_params.conn_type} table {table_name}, schema {schema or "default"}')
#         df.to_sql(name=table_name, con=engine, schema=schema, if_exists='append')
#     return schema, table_name
