from pydantic import ConfigDict, Field

from ..base import RootSchemaBaseModel, SchemaBaseModel

VERSION = "0.2"


class SchemaBaseModelV00(SchemaBaseModel):
    model_config = ConfigDict(extra="allow")


class RootSchemaBaseModelV00(RootSchemaBaseModel):
    model_config = ConfigDict(extra="allow")
    schema_version: str = Field(default=VERSION, alias="schemaVersion")
