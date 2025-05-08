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
        print(f"Fetching video information from {your_link} using pytubefix...")
        yt = YouTube(your_link) # <--- USES PYTUBEFIX OBJECT NOW

        # --- Quality selection ---
        print("\nAvailable video streams (progressive - video & audio combined):")
        available_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

        if not available_streams:
            print("No progressive MP4 streams found. Trying to get any highest resolution stream.")
            my_video = yt.streams.get_highest_resolution()
            if not my_video:
                print("Error: Could not find any suitable video stream to download.")
                return
        else:
            for i, stream in enumerate(available_streams):
                print(f"{i+1}. Resolution: {stream.resolution}, FPS: {stream.fps}, Type: {stream.mime_type}")

            while True:
                try:
                    choice = input(f"Enter the number of the desired quality (1-{len(available_streams)}), or 'h' for highest, 'l' for lowest: ").strip().lower()
                    if choice == 'h':
                        my_video = available_streams.first() # .first() after order_by desc gives highest
                        break
                    elif choice == 'l':
                        my_video = available_streams.last() # .last() after order_by desc gives lowest
                        break
                    elif choice.isdigit() and 1 <= int(choice) <= len(available_streams):
                        my_video = available_streams[int(choice)-1]
                        break
                    else:
                        print(f"Invalid input. Please enter a number between 1 and {len(available_streams)}, 'h', or 'l'.")
                except ValueError:
                    print("Invalid input. Please enter a valid number, 'h', or 'l'.")

        if not my_video: # Should not happen if logic above is correct, but as a safeguard
            print("Error selecting video stream. Aborting.")
            return

        print(f"Selected quality: Resolution: {my_video.resolution}, FPS: {my_video.fps}")
        print(f"Attempting to download to: {VIDEO_SAVE_PATH}")
        # --- End quality selection ---

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
