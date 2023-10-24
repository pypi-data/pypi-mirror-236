import enum
import importlib
import importlib.util
import json
import os
import sys
from typing import Any, List, _UnionGenericAlias, get_type_hints

import click


class FunctionArgumentsParser:
    def __get_enum_values(self, enum_cls: object) -> List[Any]:
        """Function to get enum values from an enum class"""
        return [member.value for member in enum_cls]

    def __get_field_type_str(self, field_type: Any) -> str:
        """Function to get a string representation of a field's type"""
        if isinstance(field_type, int):
            return "int"
        if isinstance(field_type, float):
            return "float"
        return "str"

    def __dataclass_to_json(self, dataclass_cls: object) -> dict:
        """Function to convert a dataclass to JSON format"""
        params = []
        type_hints = get_type_hints(dataclass_cls)

        for field_name, field_type in type_hints.items():
            is_optional = False
            values = None

            # Check if the field type is Optional (_UnionGenericAlias with None)
            if isinstance(field_type, _UnionGenericAlias) and type(None) in field_type.__args__:
                is_optional = True
                field_type = field_type.__args__[0]

            # Determine the field type string
            if issubclass(field_type, enum.Enum):
                field_type_str = "enum"
                values = self.__get_enum_values(field_type)
            else:
                field_type_str = self.__get_field_type_str(field_type)

            params.append(
                {
                    "name": field_name,
                    "optional": is_optional,
                    "type": field_type_str,
                    "values": values,
                }
            )

        return {"params": params}

    def find_and_get_json(self):
        file_names = [file_name for file_name in os.listdir(".") if os.path.isfile(file_name)]

        args_json = {}

        if "args.py" not in file_names:
            click.echo("args.py not found, creating empty args.json")
        else:
            try:
                spec = importlib.util.spec_from_file_location("args", os.getcwd() + "/args.py")
                args = importlib.util.module_from_spec(spec)
                sys.modules["args"] = args
                spec.loader.exec_module(args)
            except Exception as e:
                click.echo(f"unable to import args.py. aborting + {e}")
                exit()

            click.echo("Found args.py")
            args_json = self.__dataclass_to_json(args.FunctionArguments)

        click.echo("Creating args.json")
        with open("args.json", "w") as file:
            json.dump(args_json, file, indent=4)
        click.echo("Created args.json")

        return args_json
