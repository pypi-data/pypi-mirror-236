from __future__ import annotations
from enum import Enum
from typing import Any, List, Dict, Optional, Callable


# Enum class over all Json Types
class JsonSchemaType(Enum):
    STRING = "string"
    NUMBER = "number"
    OBJECT = "object"
    ARRAY = "array"
    BOOLEAN = "boolean"
    NULL = "null"


class ParamDescriptor:
    """
    Describes a parameter to be used in the OPENAI API.

    Attributes
    ----------
        name : str
            the parameter name
        description : str
            the parameter description
        json_type : JsonType:
            the parameter json type
        attributes_params_descriptors : list of ParamDescriptor
            the list of parameters descriptors for the attributes of the parameter
            in case the parameter is an object, defualts to None
        array_type_descriptors : list of ParamDescriptor
            the parameter descriptors for the array type in case the parameter is an array, defaults to None
        enum_values:
            the list of values in case the parameter is an enum, defaults to None
        required : bool
            whether the parameter is required or not, defaults to True

    """

    def __init__(
        self,
        name: str,
        description: str,
        json_type: JsonSchemaType,
        attributes_params_descriptors: Optional[List[ParamDescriptor]] = None,
        array_type_descriptors: Optional[List[ParamDescriptor]] = None,
        array_type_any_valid: bool = True,
        enum_values: Optional[List[Any]] = None,
        required: bool = True,
    ):
        self.name = name
        self.description = description
        self.json_type = json_type
        self.attributes_params_descriptors = attributes_params_descriptors
        self.array_type_descriptors = array_type_descriptors
        self.array_type_any_valid = array_type_any_valid
        self.enum_values = enum_values
        self.required = required

    def get_jsonapi_schema(self) -> Dict[str, Any]:
        """
        Returns the jsonapi schema for the parameter.
        """
        schema: dict[str, Any] = {
            "type": self.json_type.value,
            "description": self.description,
        }

        if (
            self.json_type == JsonSchemaType.OBJECT
            and self.attributes_params_descriptors
        ):
            schema["properties"] = {}
            schema["required"] = []
            for param in self.attributes_params_descriptors:
                schema["properties"][param.name] = param.get_jsonapi_schema()
                if param.required:
                    schema["required"].append(param.name)

        if self.json_type == JsonSchemaType.ARRAY and self.array_type_descriptors:
            items_schema = [
                desc.get_jsonapi_schema() for desc in self.array_type_descriptors
            ]
            if self.array_type_any_valid:
                schema["items"] = {"anyOf": items_schema}
            else:
                schema["items"] = [items_schema]

        if self.enum_values:
            schema["enum"] = self.enum_values

        return schema


class FuncWrapper:
    """
    Wraps a function call to be used in the OPENAI API.
    Holds the function to be called as well as the function name, its description that the agent will understand,
    and the response json schema.

    Attributes
    ----------
        function : Callable[..., Any]
            the function to be called
        name : str
            the function name
        description : str
            the function description
        params_descriptors: List[ParamDescriptor]
            the list of parameters descriptors

    Methods
    -------
        call(params: Dict[str, Any]) -> Any
            calls the function with the given parameters
        get_jsonapi_schema() -> Dict[str, Any]
            returns the jsonapi schema for the function
    """

    def __init__(
        self,
        function: Callable[..., Any],
        name: str,
        description: str,
        params_descriptors: List[ParamDescriptor],
    ):
        self.function = function
        self.name = name
        self.description = description
        self.params_descriptors = params_descriptors

    def call(self, params: Dict[str, Any]) -> Any:
        """
        Calls the function with the given parameters.

        Parameters
        ----------
            params : dict
                the parameters to be passed to the function
        """
        return self.function(**params)

    def get_json_schema(self) -> Dict[str, Any]:
        """
        Returns the jsonapi schema for the function.
        """
        schema = {
            "type": "object",
            "properties": {},
            "required": [],
        }

        for param in self.params_descriptors:
            schema["properties"][param.name] = param.get_jsonapi_schema()
            if param.required:
                schema["required"].append(param.name)

        return schema


class FunctionHandler:
    """
    Handles the functions to be used in the OPENAI API.
    Holds a list of FuncWrapper instances.

    Attributes
    ----------
        functions : List[FuncWrapper]
            the list of functions to be called
    """

    def __init__(self, functions: List[FuncWrapper] = []):
        self.functions = functions

    def function_handler(self, function_name, kwargs):
        # Check if function_name exists in functions, if not, raise UnexpectedFunctionCallException
        function_wrapper = next(
            (f for f in self.functions if f.name == function_name), None
        )
        if not function_wrapper:
            raise UnexpectedFunctionCall(function_name)

        # If the name of the current function matches the provided name
        # Call the function and return its result
        return function_wrapper.function(**kwargs)

    def get_openai_json_schema(self) -> List[Dict[str, Any]]:
        openai_functions = []
        for function in self.functions:
            function_data = {
                k: v
                for k, v in {
                    "name": function.name,
                    "description": function.description,
                    "parameters": function.get_json_schema(),
                }.items()
                if v is not None
            }

            openai_functions.append(function_data)

        return openai_functions


class UnexpectedFunctionCall(Exception):
    def __init__(self, func_name):
        message = f"Unexpected function call: {func_name}"
        super().__init__(message)
