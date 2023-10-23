from marshmallow import fields, Schema
from typing import Any, List, Type, Union

class AlwaysListField(fields.Field):
    """
    A custom Marshmallow field that ensures values passed to it for
    (de)serialization are always treated as lists.

    Attributes:
        field_type (fields.Field): The Marshmallow field to be used for (de)serialization.
    """

    def __init__(self, field_type: Union[Type[fields.Field], fields.Nested], *args: Any, **kwargs: Any) -> None:
        """
        Initialize the AlwaysListField with a given field type for (de)serialization.

        Args:
            field_type (Union[Type[fields.Field], fields.Nested]): The Marshmallow field to be used for (de)serialization.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.field_type: fields.Field = field_type

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs: Any) -> List[Any]:
        """
        Serialize the input value. If value is not a list, it's wrapped into a list.

        Args:
            value (Any): The value to be serialized.
            attr (str): The attribute/key in the original data to get the value from.
            obj (Any): The original object being serialized.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Any]: A list containing serialized data.
        """
        values = value if isinstance(value, list) else [value]
        return [self.field_type._serialize(item, attr, obj, **kwargs) for item in values]

    def _deserialize(self, value: Union[Any, List[Any]], attr: str, data: Any, **kwargs: Any) -> List[Any]:
        """
        Deserialize the input value. If value is not a list, it's wrapped into a list.

        Args:
            value (Union[Any, List[Any]]): The value to be deserialized.
            attr (str): The attribute/key in the original data to get the value from.
            data (Any): The full original data.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Any]: A list containing deserialized data.
        """
        values = value if isinstance(value, list) else [value]
        return [self.field_type._deserialize(item, attr, data, **kwargs) for item in values]
