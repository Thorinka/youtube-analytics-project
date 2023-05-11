import os

import isodate
from googleapiclient.discovery import build
from datetime import datetime
from src.video import Video


class PlayList():
    api_key: str = os.getenv('API_KEY_YOUTUBE')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self._playlist_videos = PlayList.youtube.playlistItems().list(playlistId=playlist_id,
                                                     part='snippet, contentDetails',
                                                     maxResults=50).execute()
        self._channel_id = self._playlist_videos["items"][0]["snippet"]["channelId"]
        self._playlist = PlayList.youtube.playlists().list(channelId=self._channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50).execute()
        self._video_ids = [i["contentDetails"]["videoId"] for i in self._playlist_videos["items"]]

        for playlist in self._playlist['items']:
            if playlist["id"] == self.__playlist_id:
                self.title = playlist["snippet"]["title"]

        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @property
    def total_duration(self):
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self._video_ids)).execute()
        general_duration = None

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            if not general_duration:
                general_duration = duration
            else:
                general_duration += duration

        return general_duration

    def show_best_video(self):
        video_list = []
        likes_list = []
        for v_id in self._video_ids:
            video_list.append(Video(v_id))
        for video in video_list:
            likes_list.append(int(video.likes_count))
        best_likes = max(likes_list)
        for video in video_list:
            if video.likes_count == str(best_likes):
                return video.video_url



if __name__ == '__main__':
    pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    print(pl.show_best_video())
