# standard library (this section is auto-gen from isort; see .isort.cfg)
import json
from typing import Tuple, Union

# vendor (this section is auto-gen from isort; see .isort.cfg)
import base64
import filetype
import io
import requests
import tempfile
from requests.structures import CaseInsensitiveDict


class CannotDetermineFileTypeError(ValueError):
    def __init__(self, message="Cannot determine file type"):
        self.message = message


class UnsupportedImageTypeError(ValueError):
    def __init__(self, message="Image format is unsupported"):
        self.message = message


class BadResponseError(ValueError):
    def __init__(self, message="Bad response"):
        self.message = message


def _guess_file_extension(f: Union[bytes, str]) -> str:
    kind = filetype.guess(f)
    if kind is None:
        raise CannotDetermineFileTypeError
    if not filetype.helpers.is_image(f):
        raise UnsupportedImageTypeError
    return kind.extension


def _data_uri_for_b64_img(b64_img: str, mimetype: str) -> str:
    return f"data:{mimetype};base64,{b64_img}"


class Consent:
    def __init__(self, host: str, port: int, api_key: str = None):
        self.url = f"http://{host}:{port}/v1/"
        self.api_key = api_key

    #
    # Methods
    #

    def _get_full_url(self, endpoint: str) -> str:
        # escape any erroneous prefixing like /v1 which we already have in the url
        return f"{self.url}{endpoint.replace('/v1/', '')}"

    def _get(self, endpoint: str, params: dict = None) -> Tuple[dict, CaseInsensitiveDict]:
        resp = requests.get(
            self._get_full_url(endpoint),
            params=params,
            headers=self._generate_header(),
        )
        if resp.ok:
            return json.loads(resp.text), resp.headers
        raise BadResponseError(f"GET {resp.url}: {resp.text}")

    def _patch(self, endpoint: str, data: dict = None) -> Tuple[dict, CaseInsensitiveDict]:
        resp = requests.patch(
            self._get_full_url(endpoint),
            data=data,
            headers=self._generate_header(),
        )
        if resp.ok:
            return json.loads(resp.text), resp.headers
        raise BadResponseError(f"PATCH {resp.url}: {resp.text}")

    def _post(self, endpoint: str, json_data: dict = None, data: dict = None) -> Tuple[dict, CaseInsensitiveDict]:
        resp = requests.post(
            self._get_full_url(endpoint),
            json=json_data,
            data=data,
            headers=self._generate_header(),
        )
        if resp.ok:
            return json.loads(resp.text), resp.headers
        raise BadResponseError(f"POST {resp.url}: {resp.text}")

    #
    # Misc.
    #

    def _generate_header(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def _handle_image(self, image) -> Tuple[str, str]:
        filetype = _guess_file_extension(image)
        mimetype = f"image/{filetype}"

        if isinstance(image, str):
            with open(image, "rb") as file:
                return base64.b64encode(file.read()).decode("ascii"), mimetype
        elif isinstance(image, bytes):
            return base64.b64encode(image).decode("ascii"), mimetype
        elif isinstance(
            image,
            (
                io.BufferedRandom,
                tempfile._TemporaryFileWrapper,
                io.BytesIO,
                io.BufferedReader,
            ),
        ):
            return base64.b64encode(image.read()).decode("ascii"), mimetype
        else:
            # Catch-all. In practice, _guess_file_extension() should throw on any invalid images.
            raise UnsupportedImageTypeError

    #
    # Pagination
    #

    def _paginate_get(self, endpoint: str) -> dict:
        token = ""
        while token is not None:
            data, _ = self._get(endpoint, params={"page_token": token})
            token = data["data"]["next_page_token"]
            yield data

    def _paginate_results(self, endpoint: str, data: dict) -> dict:
        # TODO: FIXME: Can this be replaced by just `_paginate_get`?
        yield data
        token = data["data"]["next_page_token"]
        while token is not None:
            data, _ = self._get(endpoint, params={"page_token": token})
            token = data["data"]["next_page_token"]
            yield data

    #
    # API
    #

    def compare_images(self, image_a, image_b) -> dict:
        """
        Compares two images and returns the similarity

        :param image_a: Image a
        :type: str, bytes, io.BufferedRandom, tempfile._TemporaryFileWrapper, io.BytesIO, io.BufferedReader
        :param image_b: Image b
        :type: str, bytes, io.BufferedRandom, tempfile._TemporaryFileWrapper, io.BytesIO, io.BufferedReader

        :return: Dictionary
        :rtype: dict
        """
        image_a_base64, image_a_mimetype = self._handle_image(image_a)
        image_b_base64, image_b_mimetype = self._handle_image(image_b)
        data, _ = self._post(
            endpoint="compare_images",
            data={
                "image_a": _data_uri_for_b64_img(image_a_base64, image_b_mimetype),
                "image_b": _data_uri_for_b64_img(image_b_base64, image_b_mimetype),
            },
        )
        return data

    def create_collection(self, collection_name: str) -> dict:
        """
        Create a new collection

        :param collection_name: Collection Name
        :type collection_name: str
        :return: Dictionary
        :rtype: dict
        """
        data, _ = self._post(endpoint=f"collections", json_data={"collection_name": collection_name})
        return data

    def create_image(self, collection_name: str, image, image_metadata: json = None) -> dict:
        """Create an image

        :param collection_name: Collection Name
        :type collection_name: str
        :param image: Image
        :type image: str, bytes, io.BufferedRandom, tempfile._TemporaryFileWrapper, io.BytesIO, io.BufferedReader
        :param image_metadata: Image metadata, defaults to None
        :type image_metadata: json, optional
        :return: Dictionary
        :rtype: dict
        """
        image_base64, image_mimetype = self._handle_image(image)
        data, _ = self._post(
            endpoint=f"collections/{collection_name}/images",
            data={
                "image": _data_uri_for_b64_img(image_base64, image_mimetype),
                "image_metadata": image_metadata,
            },
        )
        return data

    def detect_image(self, image, all_faces: bool = False) -> dict:
        """Detect an image

        :param image: Image
        :type image: str, bytes, io.BufferedRandom, tempfile._TemporaryFileWrapper, io.BytesIO, io.BufferedReader
        :param all_faces: Detect all faces, defaults to False
        :type all_faces: bool, optional
        :return: Dictionary
        :rtype: dict
        :yield: 10 results
        :rtype: Iterator[dict]
        """
        image_base64, image_mimetype = self._handle_image(image)
        data, headers = self._post(
            endpoint="detect_image",
            data={
                "image": _data_uri_for_b64_img(image_base64, image_mimetype),
                "all_faces": all_faces,
            },
        )
        if "Location" in headers:
            yield from self._paginate_results(headers["Location"], data)
        else:
            return data

    def embed_image(self, image, all_faces: bool = False) -> dict:
        """Embed an image

        :param image: Image
        :type image: str, bytes, io.BufferedRandom, tempfile._TemporaryFileWrapper, io.BytesIO, io.BufferedReader
        :param all_faces: Detect all faces, defaults to False
        :type all_faces: bool, optional
        :return: Dictionary
        :rtype: dict
        :yield: 10 results
        :rtype: Iterator[dict]
        """
        image_base64, image_mimetype = self._handle_image(image)
        data, headers = self._post(
            endpoint="embed_image",
            data={
                "image": _data_uri_for_b64_img(image_base64, image_mimetype),
                "all_faces": all_faces,
            },
        )
        if "Location" in headers:
            yield from self._paginate_results(headers["Location"], data)
        else:
            return data

    def detect_spoof_image(self, image, all_faces: bool = False) -> dict:
        """Detect a spoof image

        :param image: Image
        :type image: str, bytes, io.BufferedRandom, tempfile._TemporaryFileWrapper, io.BytesIO, io.BufferedReader
        :param all_faces: Detect all faces, defaults to False
        :type all_faces: bool, optional
        :return: Dictionary
        :rtype: dict
        :yield: 10 results
        :rtype: Iterator[dict]
        """
        image_base64, image_mimetype = self._handle_image(image)
        data, headers = self._post(
            endpoint="detect_spoof_image",
            data={
                "image": _data_uri_for_b64_img(image_base64, image_mimetype),
                "all_faces": all_faces,
            },
        )
        if "Location" in headers:
            yield from self._paginate_results(headers["Location"], data)
        else:
            return data

    def get_collection(self, collection_name: str) -> dict:
        """Returns a collection

        :param collection_name: Collection Name
        :type collection_name: str
        :return: Dictionary
        :rtype: dict
        """
        data, _ = self._get(f"collections/{collection_name}")
        return data

    def get_collections(self):
        """Returns all collections

        :yield: 10 results
        :rtype: Iterator[dict]
        """
        yield from self._paginate_get("collections")

    def search_embedding(self, collection_name: str, face_embeddings: list) -> dict:
        """_summary_

        :param collection_name: Collection Name
        :type collection_name: str
        :param face_embeddings: Face Embeddings
        :type face_embeddings: list
        :return: Dictionary
        :rtype: dict
        :yield: 10 results
        :rtype: Iterator[dict]
        """
        data, headers = self._post(
            endpoint=f"collections/{collection_name}/search_embedding",
            json_data={"face_embeddings": face_embeddings},
        )
        if "Location" in headers:
            yield from self._paginate_results(headers["Location"], data)
        else:
            return data

    def search_image(self, collection_name: str, image, all_faces: bool = False) -> dict:
        """_summary_

        :param collection_name: Collection Name
        :type collection_name: str
        :param image: Image
        :type image: str, bytes, io.BufferedRandom, tempfile._TemporaryFileWrapper, io.BytesIO, io.BufferedReader
        :param all_faces: Search all faces, defaults to False
        :type all_faces: bool, optional
        :return: Dictionary
        :rtype: dict
        :yield: 10 results
        :rtype: Iterator[dict]
        """
        image_base64, image_mimetype = self._handle_image(image)
        data, headers = self._post(
            endpoint=f"collections/{collection_name}/search",
            json_data={
                "image": _data_uri_for_b64_img(image_base64, image_mimetype),
                "all_faces": all_faces,
            },
        )
        if "Location" in headers:
            yield from self._paginate_results(headers["Location"], data)
        else:
            return data

    def update_image(self, collection_name: str, image_id: str, image_metadata: json) -> dict:
        """Update the metadata on an image

        :param collection_name: Collection _name
        :type collection_name: str
        :param image_id: Image ID
        :type image_id: str
        :param image_metadata: Image Metadata
        :type image_metadata: json
        :return: Dictionary
        :rtype: dict
        """
        data, _ = self._patch(
            endpoint=f"collections/{collection_name}/images/{image_id}",
            data={"image_metadata": image_metadata},
        )
        return data
