# marshmallow-always-list-field
This is a small package that will ensure that your marshmallow will alway contain list.

Some times you want to ensure that your marshmallow schema will always return a list, even if the input is a single item. Just to make an API response consistent.

## Installation
```bash
pip install marshmallow-always-list-field
```

## Usage
```python
from marshmallow_always_list_field import AlwaysListField

class MySchema(Schema):
    my_list = AlwaysListField(fields.String())
```

If input is:
```python
{
    "my_list": "foo"
}
```

it will result with:
```python
{
    "my_list": ["foo"]
}
```

This will work with nested fields as well.

If nested field is:
```python
class NestedSchema(Schema):
    my_list = AlwaysListField(fields.String())

class MySchema(Schema):
    nested = fields.Nested(NestedSchema)
```

and input is:
```python
{
    "nested": {
        "my_list": "foo"
    }
}
```

result will be:
```python
{
    "nested": {
        "my_list": ["foo"]
    }
}
```

Additionally you can do something like this:

```python
class NestedSchema(Schema):
    data = fields.String()

class SampleSchema(Schema):
    nested = AlwaysListField(fields.Nested(NestedSchema))

assert result == {"nested": [{"data": "hello"}]}
```

and input is:
```python
{
    "nested": {
        "data": "hello"
    }
}
```

result will be:
```python
{
    "nested": [{"data": "hello"}]
}
```

## Development
```bash
pip install -r requirements.txt
```

## Testing
```bash
pytest
```

## License
MIT

## Author
Dominik Szymanski
