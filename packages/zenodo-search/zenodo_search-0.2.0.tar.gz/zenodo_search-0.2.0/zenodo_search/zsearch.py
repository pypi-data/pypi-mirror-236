import pathlib
from typing import List
from urllib.parse import urlencode

import requests

from . import utils

BASE_RECORD_URL = 'https://zenodo.org/api/records?'
BASE_SANDBOX_URL = 'https://sandbox.zenodo.org/api/records?'


class ReadOnlyDict(dict):
    """Read-only dictionary. This is a dictionary which can be accessed as
    a normal dictionary, but cannot be modified. It is used to wrap the
    Zenodo API response, so that the user cannot modify the response."""

    __specials__ = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if key in self.__specials__:
                setattr(self, key, self.__specials__[key](value))
            else:
                if isinstance(value, dict):
                    setattr(self, key, ReadOnlyDict(value))
                else:
                    setattr(self, key, value)

    def __readonly__(self, *args, **kwargs):
        raise TypeError("Read-only dictionary, cannot modify items.")

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise TypeError("Read-only dictionary, cannot modify items.")
        super().__setattr__(name, value)

    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    clear = __readonly__
    update = __readonly__


class ZenodoFile(ReadOnlyDict):
    """Zenodo file object. Effectively a wrapper around the dictionary which is
    returned by the Zenodo API upon the query request"""

    def download(self, destination_dir=None, timeout=None):
        """Download the file from Zenodo.

        Parameters
        ----------
        destination_dir : str or pathlib.Path, optional
            Destination directory, by default None
        timeout : int, optional
            Timeout in seconds, by default None

        Returns
        -------
        pathlib.Path
            Path to the downloaded file
        """
        from .utils import download_file
        return download_file(self,
                             destination_dir=destination_dir,
                             timeout=timeout)


class ZenodoFiles(list):
    """List of ZenodoFile objects"""

    def __getitem__(self, item):
        return ZenodoFile(super().__getitem__(item))

    def download(self, destination_dir=None, timeout=None):
        """Download all registered files."""
        from .utils import download_files
        return download_files(self, destination_dir, timeout)


class ZenodoRecord(ReadOnlyDict):
    """Zenodo ZenodoRecord. Effectively a wrapper around the dictionary which is
    returned by the Zenodo API upon the query request
    """
    __specials__ = {'files': ZenodoFiles}

    def __repr__(self):
        return f'<ZenodoRecord {self.links.latest_html}: {self.metadata.title}>'

    def __str__(self):
        return self.__repr__()

    @property
    def html_badge(self, style='markdown'):
        return f'<a href="https://doi.org/{self.doi}"><img src="https://zenodo.org/badge/DOI/{self.doi}.svg" alt="DOI"></a>'

    @property
    def markdown_badge(self):
        return f'[![DOI](https://zenodo.org/badge/DOI/{self.doi}.svg)](https://doi.org/{self.doi})'

    def _repr_html_(self):
        return f'{self.html_badge} {self.metadata.title}'


class ZenodoRecords:
    """Multiple Zenodo ZenodoRecord objects"""

    def __init__(self, zenodo_records: List[ZenodoRecord], query_string: str, response):
        self._zenodo_records = zenodo_records
        self.query_string = query_string
        self.response = response

    def __repr__(self) -> str:
        return f'<ZenodoRecords ({self.query_string["q"]} with {len(self)} ZenodoRecords>'

    def __len__(self):
        return len(self._zenodo_records)

    def __getitem__(self, item):
        return self._zenodo_records[item]

    def __iter__(self):
        return iter(self._zenodo_records)


def search(search_string: str, sandbox: bool = False) -> ZenodoRecords:
    """post query to zenodo api

    Examples
    --------
    >>> import zenodo_search as zsearch
    >>> zsearch('resource_type.type:other AND creators.name:("Probst, Matthias")')
    >>> zsearch('type:dataset AND creators.affiliation:("University A" OR "Cambridge")')
    """
    search_query = {"q": search_string.replace("/", "*")}
    if sandbox:
        api_url = BASE_SANDBOX_URL + urlencode(search_query)
    else:
        api_url = BASE_RECORD_URL + urlencode(search_query)

    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information from the response
        if sandbox:
            return ZenodoRecords([ZenodoRecord(hit) for hit in data],
                                 search_query,
                                 response)
        if 'hits' in data:
            return ZenodoRecords([ZenodoRecord(hit) for hit in data['hits']['hits']],
                                 search_query,
                                 response)
    else:
        raise RuntimeError(f"Error: Request failed with status code {response.status_code}")


def search_doi(doi: str, sandbox: bool = False, parse_doi=False) -> ZenodoRecord:
    """Searches for an exact DOI

    Note:
    ----
    Since changes on zenodo backend (~Oct. 2023) the search for DOIs is not working anymore
    as initially implemented. Therefore, the search is now done by the DOI string itself without
    any prefixes added by the utils.parse_doi function. It is disabled by default, but can be
    enabled by setting the parse_doi flag to True.
    """
    if parse_doi:
        doi = utils.parse_doi(doi)
    else:
        if 'zenodo.org' in doi:
            doi = doi.rsplit('/', 1)[-1]

    r = search(f'doi:{doi}', sandbox)
    if len(r) == 0:
        raise ValueError(f'No record found for DOI: {doi}')
    assert len(r) == 1
    return r[0]


def search_keywords(keywords: List[str]):
    """Searches for all keywords"""
    kwds = ' AND '.join(f'"{k}"' for k in keywords)
    return search(f'keywords:({kwds})')
