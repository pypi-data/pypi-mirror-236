import datetime
import json

import pytest
import requests
from pydantic import BaseModel

from fermioniq.Api import (
    Api,
    ApiError,
    CancelJobResponse,
    DeleteJobResponse,
    JobResponse,
    JwtResponse,
    NoiseModel,
    RemoteConfig,
    WebsocketResponse,
)

JWT_TOKEN = "a_token"
USER_ID = "a_user_id"
BASE_URL = "http://unittests.fermioniq.nl"
X_FUNCTION_KEY = "secretkey"


def make_200_response(body: BaseModel | list | dict) -> requests.Response:
    r = requests.Response()
    r.status_code = 200
    r.headers["content-type"] = "application/json"
    if isinstance(body, BaseModel):
        r._content = body.json().encode("utf-8")
    elif isinstance(body, list):
        l = [m.dict() for m in body]
        r._content = json.dumps(l).encode("utf-8")
    elif isinstance(body, dict):
        r._content = json.dumps(body).encode("utf-8")
    else:
        raise RuntimeError("body empty")
    return r


@pytest.fixture
def api() -> Api:
    return Api(base_url=BASE_URL, api_key=X_FUNCTION_KEY)


@pytest.fixture
def patched_token(monkeypatch):
    def mocked_post(uri: str, *args, **kwargs):
        data = json.loads(kwargs.get("data", {}))

        if (
            data.get("access_token_id") != "a_token_id"
            or data.get("access_token_secret") != "a_secret"
        ):
            r = requests.Response()
            r.status_code = 403
            return r

        body = JwtResponse(
            jwt_token=JWT_TOKEN,
            user_id=USER_ID,
            expiration_date=datetime.datetime.now(),
        )
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "post", mocked_post)


def test_get_token(api, patched_token, mocker):
    """
    Tests if Api calls the login route with correct arguments
    """

    requests_spy = mocker.spy(requests, "post")

    response = api.get_token(
        access_token_id="a_token_id", access_token_secret="a_secret"
    )
    assert type(response) == JwtResponse
    assert response.jwt_token == JWT_TOKEN

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == "http://unittests.fermioniq.nl/api/login"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Content-Type",
        ]
    )
    assert request_kwargs["headers"]["Content-Type"] == "application/json"
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["data"] == json.dumps(
        {"access_token_id": "a_token_id", "access_token_secret": "a_secret"},
    )


def test_raises_api_error_on_500(api: Api, monkeypatch, mocker):
    def mocked_post(*args, **kwargs):
        r = requests.Response
        r.status_code = 500
        r.reason = "500"
        r.url = "http://whatever"
        return r

    monkeypatch.setattr(requests, "post", mocked_post)

    # requests_spy = mocker.spy(requests, "post")
    with pytest.raises(ApiError):
        api.cancel_job(token=JWT_TOKEN, job_id="1")


@pytest.mark.parametrize(
    "token_id, token_secret",
    [
        ("a_token_id", "a_wrongsecret"),
        ("a_wrong_token_id", "a_secret"),
    ],
)
def test_raises_api_error_on_get_token_invalid_creds(
    api: Api, token_id, token_secret, patched_token, mocker
):
    """
    Tests whether an ApiError is correctly raised when token_id and token_secret
    are incorrect
    """
    requests_spy = mocker.spy(requests, "post")
    with pytest.raises(ApiError):
        api.get_token(access_token_id=token_id, access_token_secret=token_secret)

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == "http://unittests.fermioniq.nl/api/login"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Content-Type",
        ]
    )
    assert request_kwargs["headers"]["Content-Type"] == "application/json"
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["data"] == json.dumps(
        {"access_token_id": token_id, "access_token_secret": token_secret},
    )


def test_get_job_by_id(api: Api, monkeypatch, mocker):
    def mocked_get(*args, **kwargs):
        body = JobResponse(
            id="1",
            user_id=USER_ID,
            creation_time=str(datetime.datetime.now()),
            status="scheduled",
            payload_digest="digest",
            status_code=-1,
        )
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "get", mocked_get)

    requests_spy = mocker.spy(requests, "get")

    response = api.get_job_by_id(token=JWT_TOKEN, job_id="1")
    assert type(response) == JobResponse
    assert response.id == "1"
    assert response.status == "scheduled"

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == "http://unittests.fermioniq.nl/api/jobs/1"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


def test_cancel_job(api: Api, monkeypatch, mocker):
    """
    Tests if Api calls the route to cancel a job correctly
    """

    def mocked_post(*args, **kwargs):
        body = CancelJobResponse(cancelled=True)
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "post", mocked_post)

    requests_spy = mocker.spy(requests, "post")

    response = api.cancel_job(token=JWT_TOKEN, job_id="1")
    assert type(response) == CancelJobResponse
    assert response.cancelled == True

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == f"http://unittests.fermioniq.nl/api/jobs/1/cancel"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


def test_delete_job(api: Api, monkeypatch, mocker):
    """
    Tests if Api calls the route to delete a job correctly
    """

    def mocked_delete(*args, **kwargs):
        body = DeleteJobResponse(job_id="1", deleted=True)
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "delete", mocked_delete)

    requests_spy = mocker.spy(requests, "delete")

    response = api.delete_job(token=JWT_TOKEN, job_id="1")
    assert type(response) == DeleteJobResponse
    assert response.job_id == "1"
    assert response.deleted == True
    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == f"http://unittests.fermioniq.nl/api/jobs/1"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


@pytest.mark.parametrize(
    "offset, limit",
    [(0, 10), (25, 50), (125, 1000)],
)
def test_get_all_jobs(api: Api, monkeypatch, mocker, offset, limit):
    """
    Test if Api calls the route to get all jobs with correct arguments and
    correct route (using offset and limit for pagination).
    """

    def mocked_get(*args, **kwargs):
        body = [
            JobResponse(
                id="1",
                user_id=USER_ID,
                creation_time=str(datetime.datetime.now()),
                status="scheduled",
                payload_digest="digest",
                status_code=-1,
            ),
        ]
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "get", mocked_get)

    requests_spy = mocker.spy(requests, "get")

    response = api.get_all_jobs(token=JWT_TOKEN, offset=offset, limit=limit)
    assert type(response) == list
    assert len(response) == 1
    assert response[0].id == "1"
    assert response[0].status == "scheduled"

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert (
        request_args[0]
        == f"http://unittests.fermioniq.nl/api/jobs?offset={offset}&limit={limit}"
    )
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


def test_get_job_results(api: Api, monkeypatch, mocker):
    """
    Tests if Api calls the route to get job results correctly.
    """

    def mocked_get(*args, **kwargs):
        body = {
            "a": "result",
        }
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "get", mocked_get)

    requests_spy = mocker.spy(requests, "get")

    response = api.get_job_results(token=JWT_TOKEN, job_id="1")
    assert type(response) == dict
    assert response["a"] == "result"

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == f"http://unittests.fermioniq.nl/api/jobs/1/results"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


def test_get_noise_models(api: Api, monkeypatch, mocker):
    """
    Tests if Api calls the route to get the Noise Models correctly
    """

    def mocked_get(*args, **kwargs):
        body = [NoiseModel(description="desc", name="name")]
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "get", mocked_get)

    requests_spy = mocker.spy(requests, "get")

    response = api.get_noise_models(token=JWT_TOKEN)
    assert type(response) == list
    assert len(response) == 1
    assert response[0].description == "desc"
    assert response[0].name == "name"

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == f"http://unittests.fermioniq.nl/api/noise-models"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


def test_get_remote_configs(api: Api, monkeypatch, mocker):
    """
    Tests if Api calls the route to get the Remote Configurations correctly
    """

    def mocked_get(*args, **kwargs):
        body = [RemoteConfig(id="1", name="2", description="3", default=True)]
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "get", mocked_get)

    requests_spy = mocker.spy(requests, "get")

    response = api.get_remote_configs(token=JWT_TOKEN)
    assert type(response) == list
    assert len(response) == 1
    assert response[0].id == "1"
    assert response[0].description == "3"

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == f"http://unittests.fermioniq.nl/api/remote-configs"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


def test_schedule_job(api: Api, monkeypatch, mocker):
    """
    Tests if Api calls the job scheduling route with correct arguments and
    the correct body.
    """

    def mocked_post(uri: str, *args, **kwargs):
        body = JobResponse(
            id="1",
            user_id=USER_ID,
            creation_time=str(datetime.datetime.now()),
            status="scheduled",
            payload_digest="digest",
            status_code=-1,
        )

        return make_200_response(body=body)

    monkeypatch.setattr(requests, "post", mocked_post)

    requests_spy = mocker.spy(requests, "post")

    response = api.schedule_job(
        token=JWT_TOKEN,
        payload={
            "key1": "value1",
            "key2": "value2",
        },
    )
    assert type(response) == JobResponse
    assert response.id == "1"
    assert response.user_id == USER_ID

    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == "http://unittests.fermioniq.nl/api/jobs"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Content-Type",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["Content-Type"] == "application/json"
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"
    assert request_kwargs["data"] == json.dumps({"key1": "value1", "key2": "value2"})


def test_get_websocket_connection(api: Api, monkeypatch, mocker):
    """
    Tests if Api calls the websocket connection GET url with the correct arguments
    """

    def mocked_get(uri: str, *args, **kwargs):
        body = WebsocketResponse(
            url="https://unittest.fermioniq.nl/websocketconnstring"
        )
        return make_200_response(body=body)

    monkeypatch.setattr(requests, "get", mocked_get)

    requests_spy = mocker.spy(requests, "get")

    response = api.get_websocket_connection(token=JWT_TOKEN, group="a_ws_group")
    assert type(response) == WebsocketResponse
    assert response.url == "https://unittest.fermioniq.nl/websocketconnstring"
    assert requests_spy.call_count == 1

    request_args = requests_spy.call_args.args
    request_kwargs = requests_spy.call_args.kwargs

    assert request_args[0] == "http://unittests.fermioniq.nl/api/websockets/a_ws_group"
    assert set(request_kwargs["headers"].keys()) == set(
        [
            "x-functions-key",
            "Authorization",
        ]
    )
    assert request_kwargs["headers"]["x-functions-key"] == X_FUNCTION_KEY
    assert request_kwargs["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"
