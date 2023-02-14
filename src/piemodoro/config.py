"""Module that handles the configuration of the application."""
from pydantic import BaseModel, Extra


class Configuration(BaseModel):
    """Class that handles the configuration of the application."""
    pomodoro: int  # minutes
    short_break: int  # minutes
    long_break: int  # minutes
    long_break_interval: int  # pomodoros

    class Config:
        extra = Extra.forbid
