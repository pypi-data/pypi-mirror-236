# Zenodo Search

Perform zenodo searches with python.

**Note**: Zenodo updated the backend. This resulted in the searches failing with the old version of this package. For
example, the doi string should not be the full doi anymore, but only the id. Some of the old search strings also don't
work anymore. This is hopefully a temporary issue and will be fixed soon.

## Installation

```bash
pip install zenodo_search
```

## Dependencies

- requests

## Usage

```python
import zenodo_search as zsearch

search_string = 'doi:8357399'
records = zsearch.search(search_string)
```

[![Open Quickstart Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matthiasprobst/zenodo_search/blob/main/examples/example.ipynb)

More examples can be found in the [examples](examples/example.ipynb) folder.
