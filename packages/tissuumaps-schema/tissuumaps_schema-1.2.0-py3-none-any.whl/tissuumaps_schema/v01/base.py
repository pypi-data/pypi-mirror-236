from pydantic import Field

from ..base import RootSchemaBaseModel

VERSION = "1.2"


class RootSchemaBaseModelV01(RootSchemaBaseModel):
    schema_version: str = Field(default=VERSION, alias="schemaVersion")
