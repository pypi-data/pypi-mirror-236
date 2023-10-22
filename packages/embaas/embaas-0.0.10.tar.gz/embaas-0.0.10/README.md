# embaas Python SDK

Python SDK for the [EMBAAS_API](https://embaas.io)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install embaas.

```bash
pip install embaas
```

## Usage

```python
from embaas import EmbaasClient

client = EmbaasClient()
client.get_embeddings(texts=["Hello World!"])
``` 

