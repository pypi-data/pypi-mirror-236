"""Handles downloading and caching of files from Zenodo."""
# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich, Switzerland.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import hashlib
import logging
import pathlib
from io import BytesIO
from json import JSONDecodeError
from typing import Dict, NamedTuple, Optional

import appdirs
import httpx
import requests
import urllib3.exceptions
from tenacity import retry, stop_after_attempt, wait_random
from tqdm import tqdm


logger = logging.getLogger(__name__)


class ZenodoSettings(NamedTuple):
    """
    Bundle the configuration for interacting with Zenodo.org.

    Attributes
    ----------
    doi : str
        The DOI of the equilibrator cache entry.
    filename : str
        The filename of the SQLite database.
    md5 : str
        The MD5 checksum of the SQLite database file.
    url : str
        The base URL of the API.

    """

    doi: str
    filename: str
    md5: str
    url: str


DEFAULT_COMPOUND_CACHE_SETTINGS = ZenodoSettings(
    doi="10.5281/zenodo.4128543",
    filename="compounds.sqlite",
    md5="9b66b85a886926d09755a66a3b452b6b",
    url="https://zenodo.org/api/",
)


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_random(min=5, max=10),
)
def find_record_by_doi(client: httpx.Client, doi: str) -> Optional[dict]:
    """Find a Zenodo record by its DOI and return all the metadata.

    Parameters
    ----------
    client: httpx.Client
        An httpx client configured with the base URL and desired timeout.
    doi : str
        The DOI of the requested entry.

    Returns
    -------
    dict
        Containing all of the metadata.

    """
    record_url = f"records/{doi.rsplit('.', 1)[1]}"

    # first verify that the record ID matches the DOI
    response = client.get(record_url)
    response.raise_for_status()
    result = response.json()
    if result["doi"] != doi:
        raise ValueError(f"Cannot find a Zenodo record with doi:{doi}.")

    # then fetch the `files` record and return it
    response = client.get(record_url + "/files")
    response.raise_for_status()
    result = response.json()
    return result


@retry(reraise=True, stop=stop_after_attempt(3), wait=wait_random(min=5, max=10))
def download_from_url(url: str, filesize: int, checksum: str) -> BytesIO:
    """Download a file from a given URL.

    Parameters
    ----------
    url : str
        The URL address of the file.
    filesize : int
        The size of the file in bytes.
    checksum : str
        The MD5 checksum.

    Returns
    -------
    BytesIO
        Bytes buffer of the downloaded file.

    """
    data = BytesIO()
    num_bytes_read = 0
    while num_bytes_read < filesize:
        headers = {}
        if num_bytes_read:
            headers["Range"] = f"bytes={num_bytes_read}-"
            print(f"continuing from bytes = {num_bytes_read}")
        response = requests.get(url, headers=headers, stream=True)
        try:
            for chunk in tqdm(
                iterable=response.iter_content(chunk_size=1024),
                total=filesize // 1024,
                unit="KB",
            ):
                data.write(chunk)
                num_bytes_read += len(chunk)
        except urllib3.exceptions.IncompleteRead as e:
            print(str(e))
            continue

    if hashlib.md5(data.getbuffer()).hexdigest() != checksum:
        raise IOError(f"MD5 mismatch while trying to download file from {url}.")

    data.seek(0)
    return data


def get_zenodo_files(settings: ZenodoSettings, timeout: float = 5.0) -> Dict[str, dict]:
    """Download all files from a Zenodo entry synchronously."""
    result_dict = {}
    with httpx.Client(base_url=settings.url, timeout=timeout) as client:
        data = find_record_by_doi(client, settings.doi)
        for d in data["entries"]:
            fname = d["key"]
            url = d["links"]["content"]
            filesize = d["size"]
            checksum = d["checksum"][4:]  # the string starts with "md5:" so we drop it
            data = download_from_url(url, filesize, checksum)
            result_dict[fname] = {
                "stream": data,
                "url": url,
                "filesize": filesize,
                "checksum": checksum,
            }
    return result_dict


def get_cached_filepath(settings: ZenodoSettings) -> pathlib.Path:
    """Get data from a file stored in Zenodo (or from cache, if available).

    Parameters
    ----------
    settings : ZenodoSettings
        Configuration for the interaction with Zenodo.org.

    Returns
    -------
    pathlib.Path
        The path to the locally cached file.

    """

    cache_directory = pathlib.Path(appdirs.user_cache_dir(appname="equilibrator"))
    cache_directory.mkdir(parents=True, exist_ok=True)

    cache_fname = cache_directory / settings.filename

    if cache_fname.exists():
        logging.info("Validate the cached copy using MD5 checksum '%s'.", settings.md5)
        if hashlib.md5(cache_fname.read_bytes()).hexdigest() == settings.md5:
            return cache_fname

    # If the checksum is not okay, it means the file is corrupted or
    # exists in an older version. Therefore, we ignore it and replace it
    # with a new version.
    logging.info("Fetching a new version of the Compound Cache from Zenodo.")
    try:
        dataframe_dict = get_zenodo_files(settings)
    except JSONDecodeError:
        raise IOError(
            "Some required data needs to be downloaded from Zenodo.org, but "
            "there is a communication problem at the "
            "moment. Please wait and try again later."
        )

    zenodo_result_dict = dataframe_dict[settings.filename]

    if zenodo_result_dict["checksum"] != settings.md5:
        raise IOError(
            f"The Zenodo entry (DOI: {settings.doi} -> "
            f"{settings.filename}) has a different MD5 checksum:"
            f"expected ({settings.md5}) != actual "
            f"({zenodo_result_dict['checksum']})."
        )

    cache_fname.write_bytes(zenodo_result_dict["stream"].getbuffer())

    logging.info(
        "Validate the downloaded copy using MD5 checksum '%s'.",
        zenodo_result_dict["checksum"],
    )
    md5 = hashlib.md5(cache_fname.read_bytes()).hexdigest()
    if md5 != settings.md5:
        raise IOError(
            f"The newly downloaded Zenodo file (DOI: {settings.doi} -> "
            f"{settings.filename}) did not pass the MD5 "
            f"checksum test: expected ({settings.md5}) != actual ({md5})."
        )

    return cache_fname
