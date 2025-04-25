import yt_dlp
import os
import time

def download_audio_from_playlist(playlist_url, output_dir="downloads", audio_format="mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best quality audio
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Save with video title as filename
        'noplaylist': True,  # Process each video individually
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,  # Convert to specified audio format
            'preferredquality': '192',  # Set audio quality
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in result:
                print(f"Found playlist with {len(result['entries'])} items.")

                # downloaded_songs = os.listdir("./Music")
                for idx, video in enumerate(result['entries'], start=1):
                    # if video["title"] in downloaded_songs:
                    #     print(f"Skipping downloading: {video['title']}")
                    #     continue
                    num_tries, backoff_time = 5, 2

                    while True:
                        try:
                            print(f"Downloading {idx}/{len(result['entries'])}: {video['title']}")
                            ydl.download([video['webpage_url']])
                            break
                        except Exception as e:
                            if num_tries <= 0:
                                print(f"Skipping {video['title']} due to an error: {e}")
                            time.sleep(backoff_time)
                            backoff_time *= 2
            else:
                ydl.download([playlist_url])  # Single video case
                
        print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PLjFTl9HTaDeoAF7ZqrBkeJ5rJw3gemotY"  # input("Enter the YouTube playlist URL: ")
    download_audio_from_playlist(playlist_url, output_dir="Music_2", audio_format="mp3")
