import json
import jsonschema


def hydrate_input_fields(formDataJsonStr, **kwargs):
    formDataStr = formDataJsonStr
    for key, value in kwargs.items():
        formDataStr = formDataStr.replace("{{" + key + "}}", value)

    return json.loads(formDataStr)


def build_input_schema_from_strada_param_definitions(param_definitions_json_str):
    # Create an empty JSON schema object
    json_schema = {"type": "object", "properties": {}, "required": []}

    param_definitions = json.loads(param_definitions_json_str)
    for param_definition in param_definitions:
        param_name = param_definition["paramName"]
        param_type = param_definition["paramType"]

        # Create a property definition for the parameter
        property_definition = {"type": param_type}

        # If the parameter has a defaultValue, add it to the schema
        if param_definition["defaultValue"]:
            property_definition["default"] = param_definition["defaultValue"]

        # Add the property definition to the JSON schema
        json_schema["properties"][param_name] = property_definition

        json_schema["required"].append(param_name)

        return json_schema


def validate_http_input(inputSchema, **kwargs):
    """
    Validate HTTP input data against a JSON schema.

    Args:
        inputSchema (dict): JSON schema representing the expected structure of the input data.
        **kwargs: Arbitrary keyword arguments representing the input data.

    Returns:
        bool: True if the input data adheres to the schema, False otherwise.
        str: A message indicating the validation result.

    Example usage:
        schema = {
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "number"}
            },
            "required": ["param1"]
        }
        result, message = validate_http_input(schema, param1="Hello", param2=42)

    """
    # Convert the input schema to a JSON string
    input_schema_str = json.dumps(inputSchema)

    # Parse the JSON schema
    schema = json.loads(input_schema_str)

    # Validate the input data against the schema
    try:
        jsonschema.validate(instance=kwargs, schema=schema)
        return True, "Input data adheres to the schema."
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)
