from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pycdp.core.events import EventStream
    from pycdp.core.target import Target


@dataclass
class TargetSession:
    """
    Represents a session with a target.
    """
    target: 'Target'
    session_id: str | None

    @classmethod
    def create(cls, target: 'Target'):
        """
        Creates a new instance of the target session.
        """
        return cls(
            target=target,
            session_id=None
        )

    async def __aenter__(self):
        """
        Allows this object to be used as a context manager.
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Closes this session when used as a context manager.
        """
        await self.close()

        if exc_type is not None:
            return False

    async def close(self):
        """
        Closes the session by detaching from the target.
        """
        method = 'Target.detachFromTarget'
        params = {
            'targetId': self.session_id
        }

        await self.send_and_await_response(
            method,
            params
        )

    def close_stream(self, stream: 'EventStream'):
        """
        Closes the stream. Calls `Target.close_stream`.
        """
        return self.target.close_stream(stream)

    async def open(self):
        """
        Opens the session by attaching to the target.
        """
        method = 'Target.attachToTarget'
        params = {
            'targetId': self.target.info.id
        }

        result = await self.send_and_await_response(
            method,
            params
        )

        self.session_id = result['sessionId']

    def open_stream(self, events: list[str]):
        """
        Opens a stream. Calls `Target.open_stream`.
        """
        return self.target.open_stream(events)

    async def send(self, method: str, params: dict = None):
        """
        Sends a message to the target. Calls `Target.send`.
        """
        params = params or {}
        params['sessionId'] = self.session_id

        return await self.target.send(
            method,
            params
        )

    async def send_and_await_response(self, method: str, params: dict = None):
        """
        Sends a message to the target and awaits a response. Calls `Target.send_and_await_response`
        """
        params = params or {}
        params['sessionId'] = self.session_id

        return await self.target.send_and_await_response(
            method,
            params
        )
