import yt_dlp
import os
from pytube import Playlist
import requests
from bs4 import BeautifulSoup
import regex
from multiprocessing import Pool
from tqdm import tqdm


def get_title_from_video_url(video_url):
    request_result = requests.get(video_url)
    soup = BeautifulSoup(request_result.text)
    raw_title_str = soup.find_all(name="title")[0]
    raw_title_str = str(raw_title_str)
    pattern = r"<title>(.*)</title>"
    result = regex.match(pattern, raw_title_str)

    if result:
        return result.group(1)

    return None

def download_song(video_url: str, yt_dl_options: dict):
    with yt_dlp.YoutubeDL(yt_dl_options) as video:
        info_dict = video.extract_info(video_url, download=False)
        video_title = info_dict["title"]
        if video_title in downloaded_songs:
            return

        video.download(video_url)

def download_playlist(playlist: Playlist, yt_dl_options: dict):
    # await tqdm.gather(*[
    #     download_song(video_url, yt_dl_options) for video_url in playlist
    # ])

    for video_url in tqdm(playlist):
        download_song(video_url, yt_dl_options)

if __name__ == "__main__":
    output_dir = "./Music"
    yt_dl_options = {
        "extract_audio": True,
        "format": "bestaudio",
        "outtmpl": f"{output_dir}/%(title)s.mp3",
        "quiet": True,
        "noprogress": True,
    }

    playlist_url = "https://www.youtube.com/playlist?list=PLjFTl9HTaDeoAF7ZqrBkeJ5rJw3gemotY"
    playlist = Playlist(playlist_url)

    downloaded_songs = [filename[:-4] for filename in os.listdir(output_dir)]
    download_playlist(playlist, yt_dl_options)
