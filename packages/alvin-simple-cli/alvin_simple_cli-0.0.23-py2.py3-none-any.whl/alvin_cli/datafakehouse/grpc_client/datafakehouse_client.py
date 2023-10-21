# ruff: noqa: A002
import grpc

from alvin_cli.config import settings
from alvin_cli.datafakehouse.grpc_generated import (
    datafakehouse_pb2 as pb2,
)
from alvin_cli.datafakehouse.grpc_generated import datafakehouse_pb2_grpc as pb2_grpc
from alvin_cli.datafakehouse.models import FORMAT, SQLDialect
from alvin_cli.utils.helper_functions import console


class InvalidSQLDialectValidationError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


def _create_channel(url: str) -> grpc.Channel:
    if ":443" not in url:
        url = url.replace("[::]", "localhost")
        return grpc.insecure_channel(url)
    call_credentials = grpc.metadata_call_credentials(
        lambda context, callback: callback(None, None),
    )
    ssl_creds = grpc.ssl_channel_credentials()
    composite_credentials = grpc.composite_channel_credentials(
        ssl_creds,
        call_credentials,
    )
    return grpc.secure_channel(url, composite_credentials)


def create_db_instance_client(*, name: str, sql_dialect: SQLDialect, format: FORMAT) -> None:
    if sql_dialect != sql_dialect.BIGQUERY:
        raise InvalidSQLDialectValidationError(f"Unable to map {sql_dialect=} to a valid value")

    assert settings.alvin_datafakehouse_api_url
    with _create_channel(settings.alvin_datafakehouse_api_url) as channel:
        stub = pb2_grpc.DatafakehouseStub(channel)
        summary_request = pb2.CreateDbInstanceRequest(name=name, sql_dialect=sql_dialect.value)
        summary_res = stub.CreateDbInstance(summary_request, metadata=[("x-api-key", settings.alvin_api_token)])

        if format == FORMAT.PLAIN:
            console.print(summary_res)
            return
        if format == FORMAT.ENV:
            console.print(f"""
export ALVIN_DB_INSTANCE_ID="{summary_res.db_instance_id}"
export ALVIN_DB_TOKEN="{summary_res.db_token}"
    """)
            return
        raise RuntimeError("Internal Error: invalid code path")
