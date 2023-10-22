"""Utility functions for the zsearch."""
import pathlib
import re
from typing import Union, Dict, List, Iterable

import requests

# error description from https://developers.zenodo.org/#http-status-codes
error_description = {200: "Request succeeded. Response included. Usually sent for GET/PUT/PATCH requests.",
                     201: "Request succeeded. Response included. Usually sent for POST requests.",
                     202: "Request succeeded. Response included. Usually sent for POST requests, where background "
                          "processing is needed to fulfill the request.",
                     204: "Request succeeded. No response included. Usually sent for DELETE requests.",
                     400: "Request failed. Error response included.",
                     401: "Request failed, due to an invalid access token. Error response included.",
                     403: "Request failed, due to missing authorization (e.g. deleting an already submitted upload or "
                          "missing scopes for your access token). Error response included.",
                     404: "Request failed, due to the resource not being found. Error response included.",
                     405: "Request failed, due to unsupported HTTP method. Error response included.",
                     409: "Request failed, due to the current state of the resource (e.g. edit a deposition which is "
                          "not fully integrated). Error response included.",
                     415: "Request failed, due to missing or invalid request header Content-Type. Error response "
                          "included.",
                     429: "Request failed, due to rate limiting. Error response included.",
                     500: "Request failed, due to an internal server error. Error response NOT included. Don’t worry, "
                          "Zenodo admins have been notified and will be dealing with the problem ASAP."
                     }

error_reason = {200: "OK",
                201: "Created",
                202: "Accepted",
                204: "No Content",
                400: "Bad Request",
                401: "Unauthorized",
                403: "Forbidden",
                404: "Not Found",
                405: "Method Not Allowed",
                409: "Conflict",
                415: "Unsupported Media Type",
                429: "Too Many Requests",
                500: "Internal Server Error"
                }


def explain_response(response: Union[int, requests.models.Response]) -> str:
    """Return the error description for a given error code."""
    if isinstance(response, requests.models.Response):
        return f'{response.status_code}: {response.reason}: {error_description[response.status_code]}'
    elif isinstance(response, int):
        return f'{response}: {error_reason[response]}: {error_description[response]}'
    raise TypeError(f"response must be of type int or requests.models.Response, not {type(response)}")


def download_file(file_dict: Dict, destination_dir: pathlib.Path = None, timeout: int = None) -> pathlib.Path:
    """Download the file from the bucket_dict to the destination directory which is the current
    directory if `destination_dir` is set to `None

    Parameters
    ----------
    file_dict : Dict
        Dictionary containing the file information
    destination_dir : pathlib.Path, optional
        Destination directory, by default None. If not None
        the directory will be created if it does not exist.
    timeout : int, optional
        Timeout in seconds, by default None

    Returns
    -------
    pathlib.Path
        Path to the downloaded file
    """
    if not isinstance(file_dict, dict):
        raise TypeError('bucket_dict must be a dictionary, not a list. Call download_files instead.')

    if 'key' not in file_dict:
        # is a bucket dict!
        response = requests.get(file_dict['links']['self'],
                                timeout=timeout)
        bucket_dict = response.json()
    else:
        bucket_dict = file_dict

    # Get the record metadata
    filename = bucket_dict['key']

    if destination_dir is not None:
        destination_dir = pathlib.Path(destination_dir)
        destination_dir.mkdir(parents=True, exist_ok=True)

        target_filename = destination_dir / filename
    else:
        target_filename = pathlib.Path(filename)

    if target_filename.exists():
        return target_filename

    with open(target_filename, 'wb') as f:
        f.write(requests.get(bucket_dict['links']['content']).content)
    return target_filename


def download_files(file_buckets: Iterable[Dict],
                   destination_dir: pathlib.Path = None,
                   timeout: int = None) -> List[pathlib.Path]:
    """Download the files from the list of bucket dictionaries to the destination directory which is here if
    set to None

    Parameters
    ----------
    file_buckets : Iterable[Dict]
        List of bucket dictionaries
    destination_dir : pathlib.Path, optional
        Destination directory, by default None. If not None
        the directory is the current directory.
    timeout : int, optional
        Timeout in seconds passed to requests.get, by default None
    """
    return [download_file(bucket_dict, destination_dir, timeout) for bucket_dict in file_buckets]


def parse_doi(doi) -> str:
    """takes doi as input, which can be the doi or Zenodo-URL"""
    if isinstance(doi, int):
        doi = f'10.5281/zenodo.{doi}'
    elif isinstance(doi, str):
        if doi.startswith('https://zenodo.org/record/'):
            doi = doi.replace('https://zenodo.org/record/', '10.5281/zenodo.')
        elif doi.startswith('https://doi.org/'):
            doi = doi.split('https://doi.org/')[1]
        elif bool(re.match(r'^\d+$', doi)):
            # pure numbers:
            doi = f'10.5281/zenodo.{doi}'
    else:
        raise TypeError(f'Invalid type for DOI: {doi}. Expected int or str')

    if not bool(re.match(r'^10\.5281/zenodo\.\d+$', doi)):
        raise ValueError(f'Invalid DOI pattern: {doi}. Expected format: 10.5281/zenodo.<number>')

    return doi
