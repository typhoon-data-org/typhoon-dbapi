import logging
from typing import Optional

from typhoon_dbapi.schemas.metadata import FieldMetadata
from typhoon_dbapi.templates.snowflake import CustomFileFormatTemplate, CopyTemplate, FileFormatType, FileFormatCompression

from typhoon_dbapi.functions.relational import execute_query
from typhoon_dbapi.hooks.dbapi_hooks import SnowflakeHook


def copy_into(
        hook: SnowflakeHook,
        table: str,
        stage_name: str,
        s3_path,
        query_params: Optional[dict] = None,
        metadata: Optional[dict] = None,

) -> str:
    fields = [FieldMetadata(name='src', type='variant')]
    file_format = CustomFileFormatTemplate(
        type=FileFormatType.JSON.value,
        compression=FileFormatCompression.AUTO.value,
        )
    audit_fields = ',\nmetadata$filename,\ncurrent_timestamp(),\nmetadata$filename'
    query = CopyTemplate(
        table=table,
        stage_name=stage_name,
        file_format=file_format,
        fields=fields,
        s3_path=s3_path,
        copy_options=None,
        audit_fields=audit_fields,
        pattern=None,
    ).render()
    logging.info(f'Executing query: {query}')
    result = execute_query(hook, query=query, batch_size=None, metadata=metadata, query_params=query_params, multi_query=False)
    logging.info(f'Results: {result}')
    next(result)
    return table
