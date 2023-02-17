import abc
from typing import Any, Optional
import json


class BaseStorage:
    state = {}

    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        self.state = state

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        return self.state


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(state, file)

    def retrieve_state(self) -> dict:
        file = open(self.file_path)
        data = json.load(file)
        return data


class State:
    """Класс для хранения состояния при работе с данными"""

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        dictionary = {key: value, }
        self.storage.save_state(dictionary)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state()
        if key in state.keys():
            return state[key]
        else:
            return None
