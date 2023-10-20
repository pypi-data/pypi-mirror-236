import asyncio
import os
import sys
import warnings
from asyncio import AbstractEventLoop
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Optional

import websockets.exceptions
from pydantic import BaseModel

from fermioniq.EmulatorJob import EmulatorJob, JobResult
from fermioniq.EmulatorMessage import EmulatorMessage
from fermioniq.logging.printing import Printer, StringMessage
from fermioniq.WebsocketHandler import WebsocketHandler, WebsocketMessage

from .Api import (
    Api,
    CancelJobResponse,
    DeleteJobResponse,
    JobResponse,
    JwtResponse,
    NoiseModel,
    RemoteConfig,
    WebsocketResponse,
)


class ClientConfig(BaseModel):
    """
    The ClientConfig class contains configuration options for the Fermioniq class.

    Attributes:
        access_token_id (str|None): API Key
            can be overwritten with environment variable FERMIONIQ_ACCESS_TOKEN_ID

        access_token_secret (str|None): API Secret
            can be overwritten with environment variable FERMIONIQ_ACCESS_TOKEN_SECRET

        ws_event_loop (asyncio.AbstractEventLoop|None): The event loop to be used by the Fermioniq class.
            If set to None, a new event loop will be created. Users can provide their own event loop if desired.

        verbosity_level (int): Level of Client verbosity. The higher the number, the more
            emulator output will be sent to the client. This has an impact on runtime performance
            and costs.

    Usage:
        custom_event_loop = asyncio.new_event_loop()
        config = ClientConfig(ws_event_loop=custom_event_loop)
        fermioniq = Client(config=config)
    """

    ws_event_loop: asyncio.AbstractEventLoop | None = None
    access_token_id: str | None = None
    access_token_secret: str | None = None
    verbosity_level: int = 0

    class Config:
        arbitrary_types_allowed = True


class Client:
    """
    The client class provides an interface to interact with the Fermioniq API. It allows users to schedule, manage,
    and retrieve the results of EmulatorJobs. Additionally, it provides websocket functionality for subscribing to job
    events and receiving updates in real-time. The class handles token management, ensuring that a valid token is
    always used when interacting with the API.

    Usage:
        config = ClientConfig()
        fermioniq = Client(config=config)

        # Schedule a new job
        job = EmulatorJob(circuit="some_circuit_definition")
        job_response = fermioniq.schedule_async(job)

        # Retrieve a specific job
        job_response = fermioniq.job(job_id="some_job_id")

        # Retrieve all jobs
        jobs_list = fermioniq.jobs()

        # Subscribe to job events
        fermioniq.subscribe_to_events(job_id="some_job_id", on_msg_callback=my_callback)
    """

    _config: ClientConfig
    _token: str | None = None
    _token_exp: datetime | None = None
    _keep_ws_open: bool = False
    _api_base_url: str
    _api_key: str | None
    _websocket_handler: WebsocketHandler
    _loop: AbstractEventLoop
    _access_token_secret: str
    _access_token_id: str

    def __init__(
        self,
        access_token_id: Optional[str] = None,
        access_token_secret: Optional[str] = None,
        verbosity_level: int = 0,
        ws_event_loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        """
        Initialize the Fermioniq instance with the given configuration.

        :param config: The Fermioniq configuration. If not provided, it will use the default configuration.
        """
        self._config = ClientConfig(
            access_token_id=access_token_id,
            access_token_secret=access_token_secret,
            verbosity_level=verbosity_level,
            ws_event_loop=ws_event_loop,
        )

        if self._config.verbosity_level < 0:
            print("Warning: Verbosity level must be positive integer in range (0, 2)")
            self._config.verbosity_level = 0
        elif self._config.verbosity_level > 2:
            print("Warning: Verbosity level must be positive integer in range (0, 2)")
            self._config.verbosity_level = 2

        access_token_id = os.getenv(
            "FERMIONIQ_ACCESS_TOKEN_ID", self._config.access_token_id
        )
        if not access_token_id:
            raise RuntimeError(
                "Missing ACCESS_TOKEN_ID. Please provide via FermioniqConfig or environment variable"
            )

        access_token_secret = os.getenv(
            "FERMIONIQ_ACCESS_TOKEN_SECRET", self._config.access_token_secret
        )
        if not access_token_secret:
            raise RuntimeError(
                "Missing ACCESS_TOKEN_SECRET. Please provide via FermioniqConfig or environment variable"
            )

        self._access_token_secret = access_token_secret
        self._access_token_id = access_token_id

        self._api_base_url = os.getenv(
            "FERMIONIQ_API_BASE_URL",
            "https://fermioniq-api-fapp-prod.azurewebsites.net",
        )
        self._api_key = os.getenv(
            "FERMIONIQ_API_KEY",
            "gCUVmJOKVCdPKRYpgk7nNWM_kTAsZfPeYTbte2sNuKtXAzFuYdj9ag==",
        )

        self._api = Api(self._api_base_url, api_key=self._api_key)

        self._loop = (
            asyncio.get_event_loop()
            if not self._config.ws_event_loop
            else self._config.ws_event_loop
        )
        self._websocket_handler = WebsocketHandler(loop=self._loop)

    def noise_models(self) -> list[NoiseModel]:
        """
        Retrieve all available noise models

        :return: A list of NoiseModel objects
        """
        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")

        return self._api.get_noise_models(token=self._token)

    def get_results(self, job_id: str) -> JobResult:
        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")
        results = self._api.get_job_results(self._token, job_id)
        return JobResult(
            job_outputs=results["emulator_output"], job_metadata=results["metadata"]
        )

    def job(self, job_id: str) -> JobResponse:
        """
        Retrieve the job with the specified job_id.

        :param job_id: The ID of the job to retrieve.
        :return: A JobResponse object containing the job details.
        """
        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")

        return self._api.get_job_by_id(self._token, job_id)

    def get_status(self, job_id: str) -> str:
        """
        Retrieve the status of the job with id job_id.

        :param job_id: The ID of the job to check the status of.
        :return: Status of the job (as a string).
        """
        job = self.job(job_id)
        return job.status

    def remote_configs(self) -> list[RemoteConfig]:
        """
        Retrieve all remote configurations.

        :return: A list of RemoteConfig objects containing the RemoteConfigs that you can use.
        """
        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")
        return self._api.get_remote_configs(self._token)

    def jobs(self, offset: int = 0, limit: int = 10) -> list[JobResponse]:
        """
        Retrieve all jobs.

        :return: A list of JobResponse objects containing the details of all jobs.
        """
        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")
        return self._api.get_all_jobs(self._token, offset=offset, limit=limit)

    def delete(self, job_id: str) -> DeleteJobResponse:
        """
        Deletes job given by id.

        :return: A DeleteJobResponse object
        """
        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")

        return self._api.delete_job(self._token, job_id)

    def cancel(self, job_id: str) -> CancelJobResponse:
        """
        Cancels a job

        :param job_id: The ID of the job to cancel.
        :return: A dict
        """
        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")

        return self._api.cancel_job(self._token, job_id=job_id)

    def schedule_and_wait(
        self,
        job: EmulatorJob,
        logger: Callable[[str], None] | None = None,
        cancel_on_interrupt: bool = True,
    ) -> JobResult:
        """
        Schedule a new job and wait for it to finish.

        :param job: The EmulatorJob to be scheduled.
        :param logger: An optional callback function for logging messages, set to python's print for unprocessed messages.
        :param cancel_on_interrupt: If True, the job will be cancelled on Keyboard interrupt signal
        :return: A JobResult object containing the results of the job.
        """
        if logger is None:
            logger = Printer().pprint

        logger(str(StringMessage("Submitting job.")))

        new_job: JobResponse = self.schedule_async(job)

        logger(str(StringMessage(f"Job scheduled. Id: '{new_job.id}'")))

        result_dict = {}

        def listener(message: EmulatorMessage) -> None:
            if logger and message.event_type == "LOG":
                logger(message.job_output)
            if message.event_type == "FINISHED":

                if message.job_status_code == 0:
                    self._ensure_valid_token()
                    if self._token:
                        if logger is not None:  # For mypy
                            logger(str(StringMessage("Retrieving results")))
                        results: dict[str, Any] = self._api.get_job_results(
                            self._token, message.job_id
                        )
                        result_dict["job_outputs"] = results["emulator_output"]
                        result_dict["job_metadata"] = results["metadata"]
                if self._websocket_handler.is_connected():
                    asyncio.get_running_loop().create_task(
                        self._websocket_handler.close()
                    )
                    self._keep_ws_open = False

                result_dict["status_code"] = (
                    message.job_status_code
                    if message.job_status_code is not None
                    else -2
                )

        self.subscribe_to_events(
            job_id=new_job.id,
            on_msg_callback=listener,
            cancel_on_interrupt=cancel_on_interrupt,
        )
        if result_dict["status_code"] != 0:
            if result_dict["status_code"] > 0:
                raise RuntimeError(
                    f"Job '{new_job.id}' finished but failed with error. Statuscode: {result_dict['status_code']}."
                )
            if cancel_on_interrupt:
                raise RuntimeError(
                    f"Job '{new_job.id}' probably got cancelled by the user. If you didn't cancel the job (e.g. by pressing Ctrl-C), then something else is wrong. Statuscode: {result_dict['status_code']}"
                )
            raise RuntimeError(
                f"There was an error with job {new_job.id}. We don't know wether it finished yet or not. Statuscode: {result_dict['status_code']}"
            )
        return JobResult(**result_dict)

    def schedule_async(self, job: EmulatorJob) -> JobResponse:
        """
        Schedule a new job asynchronously.

        :param job: The EmulatorJob to be scheduled.
        :return: A JobResponse object containing the details of the scheduled job.
        """

        self._ensure_valid_token()
        if not self._token:
            raise RuntimeError("Error getting token")

        remote_config_id: str | None = None

        remote_configs = self.remote_configs()
        if job.remote_config_name:
            remote_config = [
                rc for rc in remote_configs if rc.name == job.remote_config_name
            ]
            if not remote_config:
                available_configs = [rc.name for rc in remote_configs]
                raise RuntimeError(
                    f"Remote config with name {job.remote_config_name} does not exist. Use one of: {available_configs}"
                )

            remote_config_id = remote_config[0].id
        else:
            default_config = [rc for rc in remote_configs if rc.default]
            if not default_config:
                available_configs = [rc.name for rc in remote_configs]
                raise RuntimeError(
                    f"No config provided and no default config found. Use one of {available_configs}."
                )
            warnings.warn(
                f"No remote config provided, using default config ({default_config[0].name})."
            )
            remote_config_id = default_config[0].id

        payload: dict[str, Any] = {
            "circuit": job.circuit,
            "config": job.config,
            "verbosity_level": self._config.verbosity_level,
            "remote_config_id": remote_config_id,
        }
        if job.noise_model:
            payload["noise_model"] = job.noise_model

        remote_job = self._api.schedule_job(self._token, payload)
        job_id = remote_job.id

        job.job_id = job_id

        return remote_job

    def unsubscribe(self):
        self._keep_ws_open = False

    def subscribe_to_events(
        self,
        job_id: str,
        on_msg_callback: Callable[[EmulatorMessage], None] | None = None,
        return_as_task: bool = False,
        cancel_on_interrupt: bool = False,
        log_updates: bool = False,
        logger: Callable[[str], None] | None = None,
    ) -> None | asyncio.Task[None]:
        """
        Subscribe to job events and execute a callback function when a new message is received.

        :param job_id: The ID of the job to subscribe to.
        :param on_msg_callback: A callback function to be executed when a new message is received.
        :param return_as_task: If True, returns the task instead of executing it immediately.
        :param cancel_on_interrupt: If True, and return_as_task is False, the job will be cancelled on Keyboard interrupt signal
        :param log_updates: If True, live updates will be printed via ``logger``, or a defaul logger if ``logger`` is not set.
        :param logger: Logger to use for live updates (if set).
        :return: None if return_as_task is False, otherwise an asyncio.Task.
        """
        if log_updates and not logger:
            logger = Printer().pprint

        # First check if the job has already finished
        if self.job(job_id).status == "finished":
            return None

        def on_message(msg: WebsocketMessage):
            if on_msg_callback:
                on_msg_callback(msg.data)
            else:
                if logger and msg.data.event_type == "LOG":
                    logger(msg.data.job_output)
                if msg.data.event_type == "FINISHED":
                    if self._websocket_handler.is_connected():
                        asyncio.get_running_loop().create_task(
                            self._websocket_handler.close()
                        )
                        self._keep_ws_open = False

        if return_as_task:
            task: asyncio.Task[None] = self._loop.create_task(
                self._websocket_event_loop(group=job_id, on_message_callback=on_message)
            )
            return task
        else:
            try:
                self._loop.run_until_complete(
                    self._websocket_event_loop(
                        group=job_id, on_message_callback=on_message
                    )
                )
            except KeyboardInterrupt as e:
                self._keep_ws_open = False
                if cancel_on_interrupt:
                    result: CancelJobResponse = self.cancel(job_id=job_id)
                    # To-do: How to handle case where cancel fails?
                    if result.cancelled != True:
                        print(
                            "Error cancelling job. Either job already finished or something else went wrong.",
                            file=sys.stderr,
                        )
                    #    pass
            return None

    def _ensure_valid_token(self) -> None:
        """
        Ensure the access token is valid. If the token is invalid or expired, it will try to refresh it.
        """
        if self._token is None or self._token_expired():
            token_response: JwtResponse = self._api.get_token(
                self._access_token_id, self._access_token_secret
            )
            self._token_exp = token_response.expiration_date
            self._token = token_response.jwt_token

    def _token_expired(self) -> bool:
        """
        Check if the access token is expired.

        :return: True if the token is expired, False otherwise.
        """
        if self._token is None or self._token_exp is None:
            return True
        expired: bool = self._token_exp - datetime.now(tz=timezone.utc) < timedelta(
            days=0, seconds=1
        )
        return expired

    async def _websocket_event_loop(
        self, group: str, on_message_callback: Callable[[WebsocketMessage], None]
    ) -> None:
        """
        Asynchronous loop for handling websocket messages. Calls the on_message_callback when a new message is received.

        :param group: The group to subscribe to.
        :param on_message_callback: A callback function to be executed when a new message is received.
        """
        url: str | None = None

        def reconnect() -> str | None:
            self._ensure_valid_token()
            if not self._token:
                raise RuntimeError("Error getting token")

            try:
                ws_response: WebsocketResponse = self._api.get_websocket_connection(
                    token=self._token, group=group
                )
                return ws_response.url
            except Exception as e:
                print(e, file=sys.stderr)
                return None

        url = reconnect()
        if not url:
            raise RuntimeError("Error getting websocket connection string")

        self._keep_ws_open = True
        while self._keep_ws_open:
            try:
                if not self._websocket_handler.is_connected():
                    if url is None:
                        raise ValueError("url is None")
                    # auto reconnect. also reget token
                    await self._websocket_handler.connect(url=url)

                    joined = await self._websocket_handler.join_group(group=group)
                    if not joined:
                        raise RuntimeError(f"Error joining group: {group}")

                # joined now get data

                await self._websocket_handler.get_messages(
                    on_message=on_message_callback,
                )
            except websockets.exceptions.InvalidStatusCode as e:
                # there was some error connecting. lets try again when status code is 401 UNAUTHORIZED. maybe something
                # was temporarily wrong on the backend
                await self._websocket_handler.close(close_actual_connection=False)
                await asyncio.sleep(1)
                if e.status_code == 401:
                    url = reconnect()
                    if not url:
                        print("Error reconnecting websocket", file=sys.stderr)
                        self._keep_ws_open = False
                else:
                    self._keep_ws_open = False
                    print(
                        "Websocket receive error [InvalidStatusCode]: ",
                        e,
                        file=sys.stderr,
                    )

            except websockets.exceptions.ConnectionClosed as e:
                # backend closed connection on us.
                await self._websocket_handler.close(close_actual_connection=False)

            except websockets.exceptions.WebSocketException as e:
                await self._websocket_handler.close(close_actual_connection=False)
                print(
                    "Websocket receive error [Generic exception]: ", e, file=sys.stderr
                )
