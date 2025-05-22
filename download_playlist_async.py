import yt_dlp
import os
from pytube import Playlist
import requests
from bs4 import BeautifulSoup
import regex
from multiprocessing import Pool

num_workers = 4
output_dir = "./Music"
yt_dl_options = {
    "extract_audio": True,
    "format": "bestaudio",
    "outtmpl": f"{output_dir}/%(title)s.mp3",
    "quiet": True,
    "noprogress": True,
}
downloaded_songs = [filename[:-4] for filename in os.listdir(output_dir)]


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

def download_song(video_url: str):
    print(f"Downloading {video_url}")
    with yt_dlp.YoutubeDL(yt_dl_options) as video:
        info_dict = video.extract_info(video_url, download=False)
        video_title = info_dict["title"]
        if video_title in downloaded_songs:
            return

        video.download(video_url)
        print(f"Finished downloading{video_url}")

if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PLjFTl9HTaDeoAF7ZqrBkeJ5rJw3gemotY"
    playlist = Playlist(playlist_url)

    pool = Pool(processes=num_workers)
    pool.map(download_song, playlist)
