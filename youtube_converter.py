# youtube_converter.py
# Used pytubefix

from pytubefix import YouTube
import os

# Define base paths inside the container
BASE_DATA_PATH = "/app/data"
VIDEO_SAVE_PATH = "/app/videos"
# AUDIO_SAVE_PATH has been removed
LINKS_FILE_PATH = os.path.join(BASE_DATA_PATH, "yt_links.txt")

def ensure_dir(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def vid_dlr(your_link):
    ensure_dir(BASE_DATA_PATH)
    ensure_dir(VIDEO_SAVE_PATH)
    # ensure_dir for AUDIO_SAVE_PATH has been removed

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
        yt = YouTube(your_link)

        # --- Quality selection for video ---
        print("\nAvailable video streams (adaptive - video only, likely no sound in output):")
        video_streams = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()

        # Audio stream listing and selection has been removed
        if not video_streams:
            print("Could not find any video streams to download.")
            return

        for i, stream in enumerate(video_streams):
            print(f"{i+1}. Resolution: {stream.resolution}, FPS: {stream.fps}, Type: {stream.mime_type}")

        while True:
            try:
                choice = input(f"Enter the number of the desired video quality (1-{len(video_streams)}), or 'h' for highest, 'l' for lowest: ").strip().lower()
                if choice == 'h':
                    video_stream = video_streams.first()
                    break
                elif choice == 'l':
                    video_stream = video_streams.last()
                    break
                elif choice.isdigit() and 1 <= int(choice) <= len(video_streams):
                    video_stream = video_streams[int(choice)-1]
                    break
                else:
                    print(f"Invalid input. Please enter a number between 1 and {len(video_streams)}, 'h', or 'l'.")
            except ValueError:
                print("Invalid input. Please enter a valid number, 'h', or 'l'.")

        if not video_stream:
            print("Error selecting video stream. Aborting.")
            return

        print(f"Selected video quality: Resolution: {video_stream.resolution}, FPS: {video_stream.fps}")

        # Audio stream download has been removed

        print(f"Attempting to download video to: {VIDEO_SAVE_PATH}")
        # Downloading the selected video-only stream. The filename is kept simple.
        # You might want to generate a more descriptive name based on the video title.
        downloaded_video_path = video_stream.download(output_path=VIDEO_SAVE_PATH, filename_prefix="video_")
        
        # The downloaded file will be named something like "video_Video Title.mp4"
        # If you want a fixed name like "video_only.mp4", you can use:
        # filename = "video_only.mp4"
        # if os.path.exists(os.path.join(VIDEO_SAVE_PATH, filename)):
        #    os.remove(os.path.join(VIDEO_SAVE_PATH, filename)) # Optional: remove if exists
        # downloaded_video_path = video_stream.download(output_path=VIDEO_SAVE_PATH, filename=filename)


        # --- Merging audio and video section has been removed ---
        
        # The output_file_path is now directly the path of the downloaded video stream
        output_file_path = downloaded_video_path

        print(f"Video downloaded successfully: {os.path.basename(output_file_path)} at {output_file_path}")
        print("NOTE: This video file likely does not contain audio as only the video stream was downloaded.")

        print(f"Adding link '{your_link}' to {LINKS_FILE_PATH}...")
        with open(LINKS_FILE_PATH, 'a') as f:
            f.write(your_link + "\n")

        print("All Tasks Accomplished .. DONE")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("The link was NOT added to the library due to the error.")

# Removed VideoFileClip, AudioFileClip from moviepy.editor as they are no longer used for merging/conversion

if __name__ == "__main__":
    print(" -__________YOUTUBE VIDEO DOWNLOADER (using pytubefix) ___________-") # Title updated
    print(" -____________________________BY ASI SOLUTION ______________________________________-")
    while True:
        link = input("\nEnter Link here (or type 'exit' to quit) >>  ").strip()
        if link.lower() == 'exit':
            print("Exiting application.")
            break
        if not link:
            continue
        vid_dlr(link)
