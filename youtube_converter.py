from pytubefix import YouTube
import os
import re

BASE_DATA_PATH = "/app/data"
VIDEO_SAVE_PATH = "/app/videos"
LINKS_FILE_PATH = os.path.join(BASE_DATA_PATH, "yt_links.txt")

def ensure_dir(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', title)

def vid_dlr(your_link):
    ensure_dir(BASE_DATA_PATH)
    ensure_dir(VIDEO_SAVE_PATH)

    print("\n\nVerifying your Link Please Wait ...")
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
        safe_title = sanitize_filename(yt.title)

        # --- List progressive streams (with audio) ---
        progressive_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        # --- List adaptive video-only streams ---
        video_streams = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc()

        print("\nAvailable video streams WITH audio (progressive):")
        for i, stream in enumerate(progressive_streams):
            print(f"P{i+1}. Resolution: {stream.resolution}, FPS: {stream.fps}, Type: {stream.mime_type}")

        print("\nAvailable video streams (adaptive - video only, likely NO sound):")
        for i, stream in enumerate(video_streams):
            print(f"A{i+1}. Resolution: {stream.resolution}, FPS: {stream.fps}, Type: {stream.mime_type}")

        print("\nChoose a stream to download:")
        print("  - Enter 'P' followed by the number for progressive (with audio), e.g., 'P1'")
        print("  - Enter 'A' followed by the number for adaptive (video only), e.g., 'A1'")
        print("  - Enter 'exit' to cancel.")

        while True:
            choice = input(f"Enter your choice: ").strip().upper()
            if choice == 'EXIT':
                print("Cancelled by user.")
                return
            if choice.startswith('P') and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                if 0 <= idx < len(progressive_streams):
                    stream = progressive_streams[idx]
                    filename = f"{safe_title}_{stream.resolution}_with_audio.mp4"
                    print(f"Downloading progressive stream (with audio): {filename}")
                    output_file_path = stream.download(output_path=VIDEO_SAVE_PATH, filename=filename)
                    print(f"Video downloaded successfully: {os.path.basename(output_file_path)} at {output_file_path}")
                    break
                else:
                    print("Invalid progressive stream number.")
            elif choice.startswith('A') and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                if 0 <= idx < len(video_streams):
                    stream = video_streams[idx]
                    filename = f"{safe_title}_{stream.resolution}_video_only.mp4"
                    print(f"Downloading adaptive stream (video only): {filename}")
                    output_file_path = stream.download(output_path=VIDEO_SAVE_PATH, filename=filename)
                    print(f"Video downloaded successfully: {os.path.basename(output_file_path)} at {output_file_path}")
                    print("NOTE: This video file likely does NOT contain audio as only the video stream was downloaded.")
                    break
                else:
                    print("Invalid adaptive stream number.")
            else:
                print("Invalid input. Please enter a valid stream code (e.g., 'P1', 'A2').")

        print(f"Adding link '{your_link}' to {LINKS_FILE_PATH}...")
        with open(LINKS_FILE_PATH, 'a') as f:
            f.write(your_link + "\n")

        print("All Tasks Accomplished .. DONE")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("The link was NOT added to the library due to the error.")

if __name__ == "__main__":
    print(" -__________YOUTUBE VIDEO DOWNLOADER (using pytubefix) ___________-")
    print(" -____________________________BY ASI SOLUTION ______________________________________-")
    while True:
        link = input("\nEnter Link here (or type 'exit' to quit) >>  ").strip()
        if link.lower() == 'exit':
            print("Exiting application.")
            break
        if not link:
            continue
        vid_dlr(link)
