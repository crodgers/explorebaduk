import json
import logging

from marshmallow import ValidationError
from explorebaduk.constants import AUTH, CHALLENGE, MessageType
from explorebaduk.exceptions import AuthenticationError, InvalidMessageError
from explorebaduk.handlers.auth import handle_auth
from explorebaduk.handlers.challenge import handle_challenge
from explorebaduk.message import parse_message, InvalidMessageError

logger = logging.getLogger("explorebaduk")


async def handle_message(ws, message: str):
    logger.info("handle_message")

    try:
        message_type, data = parse_message(message)
        message_type = MessageType(message_type)

        if message_type is MessageType.AUTH:
            await handle_auth(ws, data)

        elif message_type is MessageType.CHALLENGE:
            await handle_challenge(ws, data)

        else:
            await ws.send(f"ERROR {message_type}: not implemented")

    except (AuthenticationError, InvalidMessageError, ValidationError) as err:
        return await ws.send(f"ERROR {err}")

    except json.decoder.JSONDecodeError as err:
        return await ws.send(f"ERROR {err.msg}: line {err.lineno} column {err.colno} (char {err.pos})")
