import base64
from pydantic import BaseModel
from typing import TypeVar, Type

T = TypeVar("T", bound=BaseModel)


class PydanticConverter:

    @staticmethod
    def pydantic_to_base64str(schema: T) -> str:
        schema_json = schema.model_dump_json()
        schema_json_encoded = schema_json.encode(encoding="utf-8")
        schema_base64str = base64.b64encode(schema_json_encoded)
        return schema_base64str.decode("utf-8")

    @staticmethod
    def base64str_to_pydantic(base64_str: str, output_schema: Type[T]) -> T:
        json_bytes = base64.b64decode(base64_str)
        json_str = json_bytes.decode("utf-8")
        return output_schema.model_validate_json(json_str)
