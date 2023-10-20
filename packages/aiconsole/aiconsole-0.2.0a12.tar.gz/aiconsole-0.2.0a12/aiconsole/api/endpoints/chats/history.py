import asyncio
import os
import logging
from datetime import datetime
from typing import Callable
from fastapi import APIRouter, status, Response, Depends
from aiconsole import projects
from aiconsole.api.json_file_operations import json_read, json_write
from aiconsole.chat.types import Chat

router = APIRouter()
_log = logging.getLogger(__name__)


@router.delete("/history/{chat_id}")
def delete_history(chat_id: str):
    file_path = os.path.join(projects.get_history_directory(), f"{chat_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        return Response(
            status_code=status.HTTP_200_OK,
            content="Chat history deleted successfully",
        )
    else:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Chat history not found",
        )

@router.get("/history/{chat_id}")
def get_history(chat_id: str, get_json: Callable = Depends(json_read)):
    file_path = os.path.join(projects.get_history_directory(), f"{chat_id}.json")

    return get_json(file_path=file_path, empty_obj={})

history_lock = asyncio.Lock()

@router.post("/history")
async def save_history(chat: Chat, store_json: Callable = Depends(json_write), get_json: Callable = Depends(json_read)):
    """
    Saves the history of the chat to <history_dir>/<chat.id>.json
    """

    async with history_lock:

        history_directory = projects.get_history_directory()
        headline = None

        file_path = os.path.join(history_directory, f"{chat.id}.json")

        if os.path.exists(file_path):
            history = get_json(file_path=file_path, empty_obj={})
            headline = history["headline"] if history and history.get("headline", None) else headline

        chat_data = {
            "id": chat.id,
            "auto_run": chat.auto_run,
            "timestamp": datetime.now().isoformat(),
            "messages": [message.model_dump() for message in chat.messages],
            "headline": headline
        }
        store_json(
            directory=projects.get_history_directory(),
            file_name=f"{chat.id}.json",
            content=chat_data
        )
        return Response(
            status_code=status.HTTP_201_CREATED,
            content="Chat history saved successfully",
        )


