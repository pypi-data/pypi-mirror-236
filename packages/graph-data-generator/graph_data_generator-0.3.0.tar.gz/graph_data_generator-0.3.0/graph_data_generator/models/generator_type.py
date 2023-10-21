from enum import Enum, unique
import datetime

@unique
class GeneratorType(Enum):
    UNKNOWN = 0,
    BOOL = 1,
    INT = 2,
    FLOAT = 3,
    STRING = 4,
    DATETIME = 5,
    ASSIGNMENT = 6,
    # RELATIONSHIP = 7,
    FUNCTION = 8,
    REFERENCE = 9

    @staticmethod
    def type_from_string(aType: str):
        type = aType.lower()
        if type == "string":
            return GeneratorType.STRING
        elif type == "int" or type == "integer":
            return GeneratorType.INT
        elif type == "float":
            return GeneratorType.FLOAT
        elif type =="function":
            return GeneratorType.FUNCTION
        elif type == "datetime":
            return GeneratorType.DATETIME
        elif type == "bool":
            return GeneratorType.BOOL
        elif type == "assignment":
            return GeneratorType.ASSIGNMENT
        # elif type == "relationship":
        #     return GeneratorType.RELATIONSHIP
        elif type == "reference":
            return GeneratorType.REFERENCE
        else:
            raise TypeError("Type not supported")
    
    @staticmethod
    def type_from_value(value: any):
        if isinstance(value, str):
            return GeneratorType.STRING
        elif isinstance(value, int):
            return GeneratorType.INT
        elif isinstance(value, float):
            return GeneratorType.FLOAT
        elif isinstance(value, bool):
            return GeneratorType.BOOL
        elif isinstance(value, datetime.datetime):
            return GeneratorType.DATETIME
        else:
            # Can't infer FUNCTION or REFERENCE types from value alone
            return GeneratorType.UNKNOWN

    def to_string(self) -> str:
        """
        Convert a GeneratorType enum value to its corresponding string representation.

        Returns:
            str: The string representation of the GeneratorType enum value.

        Raises:
            TypeError: If the GeneratorType enum value is not supported.
        """
        type_map = {
            GeneratorType.STRING: "String",
            GeneratorType.INT: "Integer",
            GeneratorType.FLOAT: "Float",
            GeneratorType.FUNCTION: "Function",
            GeneratorType.DATETIME: "Datetime",
            GeneratorType.BOOL: "Bool",
            GeneratorType.ASSIGNMENT: "Assignment",
            # GeneratorType.RELATIONSHIP: "Relationship"
            GeneratorType.REFERENCE: "Reference"
        }
        result = type_map.get(self, None)
        if result is None:
            return "Unknown"
        return result
