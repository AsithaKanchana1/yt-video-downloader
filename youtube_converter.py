# youtube_converter.py
# Used pytubefix

# ---- The _default_clients section for pytube is no longer needed and can be removed or commented out ----
# from pytube.innertube import _default_clients
# _default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
# ... (rest of the _default_clients lines)
# ---- END OF PYTUBE FIX SECTION ----

from moviepy.editor import VideoFileClip
from pytubefix import YouTube # <--- CHANGE HERE
import os

# Define base paths inside the container
BASE_DATA_PATH = "/app/data"
VIDEO_SAVE_PATH = "/app/videos"
AUDIO_SAVE_PATH = "/app/songs"
LINKS_FILE_PATH = os.path.join(BASE_DATA_PATH, "yt_links.txt")

def ensure_dir(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def vid_dlr(your_link):
    ensure_dir(BASE_DATA_PATH)
    ensure_dir(VIDEO_SAVE_PATH)
    ensure_dir(AUDIO_SAVE_PATH)

    print("\n\n\nVerifying your Link Please Wait ...")
    all_Links_lst = []
    
    if not os.path.exists(LINKS_FILE_PATH):
        with open(LINKS_FILE_PATH, 'w') as f:
            pass 
        print(f"Created new links file at: {LINKS_FILE_PATH}")

    with open(LINKS_FILE_PATH, "r") as f:
        all_links_content = f.read()
        if all_links_content:
            all_Links_lst = [line for line in all_links_content.split("\n") if line.strip()]      
    
    if your_link in all_Links_lst:
        print(f"Link '{your_link}' already processed and present in your Library.")
        return
            
    print(f"Link '{your_link}' not found in library. Proceeding with download.")
    
    try:
        print(f"Downloading Video from {your_link} using pytubefix...") # Updated to pytubefix 
        yt = YouTube(your_link) # <--- USES PYTUBEFIX OBJECT NOW
        my_video = yt.streams.get_highest_resolution()
        
        print(f"Attempting to download to: {VIDEO_SAVE_PATH}")
        out_file_path = my_video.download(output_path=VIDEO_SAVE_PATH)
        
        vid_name = os.path.basename(out_file_path)
        print(f"Video downloaded successfully: {vid_name} at {out_file_path}")
        
        base_vid_name, _ = os.path.splitext(vid_name)
        vidmp3_name = base_vid_name + ".mp3"
        
        print(f"Converting '{vid_name}' into Audio '{vidmp3_name}'...")
        mp4_file_full_path = os.path.join(VIDEO_SAVE_PATH, vid_name)
        mp3_file_full_path = os.path.join(AUDIO_SAVE_PATH, vidmp3_name)
        
        if not os.path.exists(mp4_file_full_path):
            print(f"ERROR: Downloaded video file not found at '{mp4_file_full_path}' for conversion.")
            return

        videoclip = VideoFileClip(mp4_file_full_path)
        audioclip = videoclip.audio
        audioclip.write_audiofile(mp3_file_full_path)
        audioclip.close()
        videoclip.close()
        
        print(f"Conversion complete. Audio saved to: {mp3_file_full_path}")
        
        print(f"Adding link '{your_link}' to {LINKS_FILE_PATH}...")
        with open(LINKS_FILE_PATH, 'a') as f:
            f.write(your_link + "\n")

        print("All Tasks Accomplished .. DONE")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("The link was NOT added to the library due to the error.")

if __name__ == "__main__":
    print(" -__________YOUTUBE VIDEO DOWNLOADER & AUDIO CONVERTER (using pytubefix) ___________-")
    print(" -____________________________BY ASI SOLUTION ______________________________________-")
    while True: 
        link = input("\nEnter Link here (or type 'exit' to quit) >>  ").strip()
        if link.lower() == 'exit':
            print("Exiting application.")
            break
        if not link:
            continue
        vid_dlr(link)
