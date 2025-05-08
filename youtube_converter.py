# youtube_converter.py
# Used pytubefix

from moviepy.editor import VideoFileClip
from pytubefix import YouTube
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
        yt = YouTube(your_link)

        # --- Quality selection ---
        print("\nAvailable video streams (adaptive - video only):")
        video_streams = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()

        print("\nAvailable audio streams (audio only):")
        audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
        if not video_streams or not audio_streams:
            print("Could not find video or audio streams.")
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

        # Select the best available audio stream
        audio_stream = audio_streams.first()
        print(f"Selected audio quality: Bitrate {audio_stream.abr}")

        print(f"Attempting to download video to: {VIDEO_SAVE_PATH}")
        video_file_path = video_stream.download(output_path=VIDEO_SAVE_PATH, filename="video_only")
        print(f"Attempting to download audio to: {AUDIO_SAVE_PATH}")
        audio_file_path = audio_stream.download(output_path=AUDIO_SAVE_PATH, filename="audio_only")
        # --- End quality selection ---

        # --- Merge audio and video using MoviePy ---
        print("Merging audio and video...")
        video_clip = VideoFileClip(video_file_path)
        audio_clip = AudioFileClip(audio_file_path)
        final_clip = video_clip.set_audio(audio_clip)

        output_file_path = os.path.join(VIDEO_SAVE_PATH, "final_video.mp4")
        final_clip.write_videofile(output_file_path, codec="libx264", audio_codec="aac")

        video_clip.close()
        audio_clip.close()
        final_clip.close()
        # Remove temporary audio and video files
        os.remove(video_file_path)
        os.remove(audio_file_path)

        print(f"Video downloaded and merged successfully: {output_file_path}")

        print(f"Adding link '{your_link}' to {LINKS_FILE_PATH}...")
        with open(LINKS_FILE_PATH, 'a') as f:
            f.write(your_link + "\n")

        print("All Tasks Accomplished .. DONE")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("The link was NOT added to the library due to the error.")

from moviepy.editor import VideoFileClip, AudioFileClip

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
