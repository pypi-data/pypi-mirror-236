# jsonencoder

[jsonencoder](https://github.com/gonzalo123/jsonencoder)

## Install

```commandline
pip install jsonencoder-gonzalo123
```

## Usage

```python
import json
from jsonencoder import DefaultEncoder

json.dumps(data, cls=DefaultEncoder)
```