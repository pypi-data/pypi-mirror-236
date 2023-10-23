# CLassAttributeModelGenerator

Given a nested dict create a hierarchical object model.

Optionally provide models in [YAML](https://yaml.org) or [JSON](https://www.json.org) format.

Some would say this is just a dict-wrapper.


### Example: Loading a nested dict

```python3
    >>> data = dict(obj=dict(foo="bar", spam="eggs", a_list=[1,2,3]))
    >>> data
    {'obj': {'foo': 'bar', 'spam': 'eggs', 'a_list': [1, 2, 3]}}
    >>> x = clamg.unpack(data)
    >>> x
    <clamg(obj=<obj(foo=bar, spam=eggs, a_list=[1, 2, 3])>)>
    >>> x.obj.foo
    'bar'
```


### Example: Loading YAML

```python3
    >>> SAMPLE_YAML = """\
    ... obj:
    ...   yaml: yes
    ...   foo: bar
    ...   spam: eggs
    ...   a_list:
    ...     - 1
    ...     - 2
    ...     - 3
    ... """
    >>> clamg.loads(SAMPLE_YAML)
    <clamg(obj=<obj(yaml=True, foo=bar, spam=eggs, a_list=[1, 2, 3])>)>
```


### Example: Loading JSON

```python3
    >>> SAMPLE_JSON = '{"obj": {"json": "yes", "foo": "bar", "spam": "eggs", "a_list": [1,2,3]}}'
    >>> clamg.loads(SAMPLE_JSON)
    <clamg(obj=<obj(json=yes, foo=bar, spam=eggs, a_list=[1, 2, 3])>)>
```


It has occasionally proven useful when working with deeply nested structures.
