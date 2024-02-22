"""Some functions to make things smooth"""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clear_stream(stream: TextIO):
    """Clear the content of a stream """
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)
