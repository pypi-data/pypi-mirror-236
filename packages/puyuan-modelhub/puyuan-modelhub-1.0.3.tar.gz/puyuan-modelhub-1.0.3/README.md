# Description
ModelhubClient: A Python client for the Modelhub API

# Installation

## Install from PyPI
```shell
pip install puyuan_modelhub
```

## Install from source

```shell
git clone https://github.com/puyuantech/modelhub
python setup.py build bdist_wheel
pip install dist/*.whl
```
# Usage 

## Client side

Initialize a ModelhubClient
```python
from modelhub import ModelhubClient

client = ModelhubClient(
    host="http://*****:*****/", user_name="****", user_password="*****"
)
```


Get supported Models

```python
client.supported_models
```

Get model supported params

```python
client.get_supported_params("Minimax")
```

Chat with model

```python
client.chat("Hello?", model="m3e")
```

Get model embeddings

```python
client.get_embeddings(["你好", "Hello"], model="m3e")
```
## Server side

Start server in 4 lines:

```python
from modelhub.server import start_server
import yaml

# load config
config = yaml.xxxx
# start server
start_server(config)
```

config file example:

```yaml
from modelhub.server import start_server
import yaml

# load config
config = yaml.xxxx
# start server
start_server(config)
```

Chat Params:

```python
class ChatParams(BaseModel):
    prompt: str
    model: str
    auth: AuthParams
    stream: bool = True
    parameters: Dict[str, Any] = {}
```
# Examples

# Contact
