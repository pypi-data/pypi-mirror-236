import datetime
import json
from typing import Any, Callable

import pytest

from fermioniq import Client, EmulatorJob, EmulatorMessage, JobResult
from fermioniq.Api import JobResponse, JwtResponse, RemoteConfig, WebsocketResponse
from fermioniq.unit_tests.utils import qiskit_bell_pair
from fermioniq.WebsocketHandler import WebsocketMessage

REMOTE_JOB_ID = "jr1"
USER_ID = "a_user_id"


class FakeWebsocketHandler:
    """
    Overwrite of fermioniq/WebsocketHandler.py
    """

    _connected: bool

    def __init__(self, *args, **kwargs):
        self._connected = False

    def is_connected(self):
        return self._connected

    async def close(self, close_actual_connection: bool = True):
        self._connected = False

    async def join_group(self, group: str) -> bool:
        return group == REMOTE_JOB_ID

    async def connect(self, url: str):
        self._connected = True

    async def get_messages(self, on_message: Callable[[WebsocketMessage], None]):

        messages = [
            WebsocketMessage(
                type="message",
                fromUserId=USER_ID,
                group=REMOTE_JOB_ID,
                dataType="json",
                data=EmulatorMessage(
                    message_type="event",
                    event_type="STARTED",
                    ts=str(datetime.datetime.now()),
                    job_id=REMOTE_JOB_ID,
                    job_output="msg1",
                ),
            ),
            WebsocketMessage(
                type="message",
                fromUserId=USER_ID,
                group=REMOTE_JOB_ID,
                dataType="json",
                data=EmulatorMessage(
                    message_type="event",
                    event_type="LOG",
                    ts=str(datetime.datetime.now()),
                    job_id=REMOTE_JOB_ID,
                    job_output=json.dumps(
                        {
                            "__ClientMessage__": {
                                "name": "StringMessage",
                                "content": {"message": "msg2"},
                            }
                        },
                    ),
                ),
            ),
            WebsocketMessage(
                type="message",
                fromUserId=USER_ID,
                group=REMOTE_JOB_ID,
                dataType="json",
                data=EmulatorMessage(
                    message_type="event",
                    event_type="FINISHED",
                    ts=str(datetime.datetime.now()),
                    job_id=REMOTE_JOB_ID,
                    job_output="msg3",
                    job_status_code=0,
                ),
            ),
        ]

        for message in messages:
            on_message(message)


class FakeApi:
    """
    Overwrite of fermioniq/Api.py
    """

    def __init__(*args, **kwargs):
        pass

    def get_token(self, access_token_id: str, access_token_secret: str) -> JwtResponse:
        return JwtResponse(
            jwt_token="a_token",
            user_id=USER_ID,
            expiration_date=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(minutes=1),
        )

    def get_remote_configs(self, token: str) -> list[RemoteConfig]:
        return [
            RemoteConfig(
                id="rc1",
                name="remote conf",
                description="desc",
                default=True,
            ),
            RemoteConfig(
                id="rc2",
                name="remote conf2",
                description="desc2",
                default=False,
            ),
        ]

    def schedule_job(self, token: str, job: EmulatorJob) -> JobResponse:
        return JobResponse(
            id=REMOTE_JOB_ID,
            user_id=USER_ID,
            creation_time=str(datetime.datetime.now()),
            status="scheduled",
            payload_digest="digest",
            status_code=-1,
        )

    def get_job_by_id(self, token: str, job_id: str) -> JobResponse:
        return JobResponse(
            id=REMOTE_JOB_ID,
            user_id=USER_ID,
            creation_time=str(datetime.datetime.now()),
            status="scheduled",
            payload_digest="digest",
            status_code=-1,
        )

    def get_job_results(self, token: str, job_id: str) -> dict[str, Any]:
        return {
            "status_code": 0,
            "emulator_output": [{"output": "output_val", "config": "0"}],
            "metadata": {
                "metadata1": "metadata_value1",
                "unique_configs": {"0": "config_1"},
            },
        }

    def get_websocket_connection(self, token: str, group: str) -> WebsocketResponse:
        return WebsocketResponse(url="ws://unittest.fermioniq.nl/wsstr")


@pytest.fixture
def patched_client(monkeypatch):
    """
    Return patched client.

    We overwrite the _api (original: fermioniq/Api.py) and _websocket_handler (original: fermioniq/WebsocketHandler.py)
    functions with our Mocks to simulate interaction with the outter world.
    """
    client = Client(
        access_token_id="a_access_token_id",
        access_token_secret="a_access_token_secret",
    )

    monkeypatch.setattr(client, "_api", FakeApi())
    monkeypatch.setattr(client, "_websocket_handler", FakeWebsocketHandler())

    return client


def test_async_scheduling_basic_flow(
    patched_client: Client,
):
    """
    This test checks whether the good flow of job scheduling works as expected when using more low level functionality.
    """

    bell_pair = qiskit_bell_pair()

    job = EmulatorJob(circuit=bell_pair, remote_config_name="remote conf")
    assert job.job_id == None

    number_messages_received = 0

    def on_emulator_message(message: EmulatorMessage):

        nonlocal number_messages_received

        assert message.job_id == REMOTE_JOB_ID

        number_messages_received += 1

        if message.event_type == "STARTED":

            assert message.job_status_code == -1
            assert message.job_output == "msg1"

        elif message.event_type == "LOG":

            assert message.job_status_code == -1

            job_output = json.dumps(
                {
                    "__ClientMessage__": {
                        "name": "StringMessage",
                        "content": {"message": "msg2"},
                    }
                }
            )

            assert message.job_output == job_output

        elif message.event_type == "FINISHED":

            assert message.job_status_code == 0
            assert message.job_output == "msg3"

            # results = client.get_results(message.job_id)
            patched_client.unsubscribe()

    remote = patched_client.schedule_async(job=job)

    # remote id is correctly assigned
    assert remote.id == "jr1"

    # EmulatorJob job id is assigned
    assert job.job_id == "jr1"

    patched_client.subscribe_to_events(
        job_id=remote.id, on_msg_callback=on_emulator_message
    )

    assert number_messages_received == 3


def test_schedule_and_wait(
    patched_client: Client,
    mocker,
):
    """
    This test checks whether the good flow of a simple job scheduling works as expected when
    using the `schedule_and_wait` function
    """

    bell_pair = qiskit_bell_pair()

    job = EmulatorJob(circuit=bell_pair, remote_config_name="remote conf")
    assert job.job_id == None

    schedule_job_spy = mocker.spy(patched_client._api, "schedule_job")
    get_job_results_spy = mocker.spy(patched_client._api, "get_job_results")

    ws_close_spy = mocker.spy(patched_client._websocket_handler, "close")
    ws_connect_spy = mocker.spy(patched_client._websocket_handler, "connect")
    ws_join_group_spy = mocker.spy(patched_client._websocket_handler, "join_group")

    result = patched_client.schedule_and_wait(job=job, logger=lambda _: None)

    assert ws_close_spy.call_count == 1
    ws_connect_spy.assert_called_once_with("ws://unittest.fermioniq.nl/wsstr")
    ws_join_group_spy.assert_called_once_with(REMOTE_JOB_ID)

    # check if job has been scheduled with correct data
    assert schedule_job_spy.call_count == 1

    schedule_job_args = schedule_job_spy.call_args.args

    assert schedule_job_args[0] == "a_token"

    assert set(schedule_job_args[1].keys()) == {
        "circuit",
        "config",
        "verbosity_level",
        "remote_config_id",
    }

    assert schedule_job_args[1]["config"][0]["qubits"] == ["0", "1"]
    assert schedule_job_args[1]["circuit"][0] == "__compressed__"

    # should we test here that we compress correctly or is that part
    # of testing emulator job?
    assert type(schedule_job_args[1]["circuit"][1]) == str

    assert schedule_job_args[1]["verbosity_level"] == 0
    assert schedule_job_args[1]["remote_config_id"] == "rc1"

    assert get_job_results_spy.call_count == 1

    assert result.status_code == 0
    assert len(result.job_outputs) == 1
    assert result.job_outputs[0]["output"] == "output_val"
    assert (
        result.job_outputs[0]["config"] == "config_1"
    )  # Should have been populated from unique_configs
    assert result.job_metadata["metadata1"] == "metadata_value1"
    assert "unique_configs" not in result.job_metadata  # Should have been popped by now
