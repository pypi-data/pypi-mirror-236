import pytest
from marshmallow import fields, Schema, ValidationError
from src.always_list_field import AlwaysListField

class SampleSchema(Schema):
    data = AlwaysListField(fields.String())

def test_serialize_single_value():
    schema = SampleSchema()
    result = schema.dump({"data": "hello"})
    assert result == {"data": ["hello"]}

def test_serialize_list_value():
    schema = SampleSchema()
    result = schema.dump({"data": ["hello", "world"]})
    assert result == {"data": ["hello", "world"]}

def test_deserialize_single_value():
    schema = SampleSchema()
    result = schema.load({"data": "hello"})
    assert result == {"data": ["hello"]}

def test_deserialize_list_value():
    schema = SampleSchema()
    result = schema.load({"data": ["hello", "world"]})
    assert result == {"data": ["hello", "world"]}

def test_deserialize_invalid_type():
    schema = SampleSchema()

    with pytest.raises(ValidationError):
        schema.load({"data": 123})

    with pytest.raises(ValidationError):
        schema.load({"data": ["hello", 123]})

def test_nested_field():
    class NestedSchema(Schema):
        data = fields.String()

    class SampleSchema(Schema):
        nested = AlwaysListField(fields.Nested(NestedSchema))

    schema = SampleSchema()
    result = schema.load({"nested": {"data": "hello"}})
    assert result == {"nested": [{"data": "hello"}]}
