import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY_YOUTUBE')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализирует id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = self.channel["items"][0]["snippet"]["title"]
        self.channel_description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscribe_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.views_count = self.channel["items"][0]["statistics"]["viewCount"]


    def __str__(self):
        """
        Возвращает информацию об объекте класса для пользователей в формате <название_канала> (<ссылка_на_канал>)
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        Возвращает сумму подписчиков subscribe_count двух объектов класса Channel
        """
        return int(self.subscribe_count) + int(other.subscribe_count)

    def __sub__(self, other):
        """
        Возвращает разницу подписчиков subscribe_count двух объектов класса Channel
        """
        return int(self.subscribe_count) - int(other.subscribe_count)

    def __gt__(self, other):
        """
        Возвращает True, если первый объект self больше объекта other
        """
        return int(self.subscribe_count) > int(other.subscribe_count)

    def __ge__(self, other):
        """
        Возвращает True, если первый объект self больше или равен объекту other
        """
        return int(self.subscribe_count) >= int(other.subscribe_count)

    def __lt__(self, other):
        """
        Возвращает True, если первый объект self меньше объекту other
        """
        return int(self.subscribe_count) < int(other.subscribe_count)

    def __le__(self, other):
        """
        Возвращает True, если первый объект self меньше или равен объекту other
        """
        return int(self.subscribe_count) <= int(other.subscribe_count)

    def __eq__(self, other):
        """
        Возвращает True, если первый объект self равен объекту other
        """
        return int(self.subscribe_count) == int(other.subscribe_count)

    def print_json(self, dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return self.print_json(channel)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube


    def to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as json_file:
            json_file.write(json.dumps(self.channel, indent=2, ensure_ascii=False))

