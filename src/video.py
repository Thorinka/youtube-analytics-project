import json
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Video:
    """Класс для видео"""
    api_key: str = os.getenv('API_KEY_YOUTUBE')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        """Экземпляр инициализирует id видео. Дальше все данные будут подтягиваться по API."""
        try:
            self.__video_id = video_id
            self.video = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=video_id).execute()

            self.video_name = self.video["items"][0]["snippet"]["title"]
            self.video_url = f"https://www.youtu.be/channel/{self.__video_id}"
            self.view_count = self.video["items"][0]["statistics"]["viewCount"]
            self.likes_count = self.video["items"][0]["statistics"]["likeCount"]
        except IndexError as err:
            self.__video_id = video_id
            self.video = None

            self.video_name = None
            self.video_url = None
            self.view_count = None
            self.likes_count = None

    def __str__(self):
        """
        Возвращает информацию об объекте класса для пользователей в формате <название_канала> (<ссылка_на_канал>)
        """
        return f"{self.video_name}"


class PLVideo(Video):
    """
    Класс для видео из плейлиста
    """
    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализирует id видео и плейлиста. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self.__playlist_id = playlist_id
