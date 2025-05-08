# YouTube Video Downloader (Dockerized)

This project provides a Python script, packaged in a Docker container, to download YouTube videos with user-selectable quality. It uses `pytubefix` for reliable YouTube video downloading, including adaptive streams for higher resolutions.

**Important Note**: The current version of the script in the `main` branch downloads video streams. For higher resolutions, these are often video-only (adaptive) streams, meaning the **downloaded video file might not contain audio**. If you require video with audio, you would need to modify the script to also download and merge an audio stream, or use a branch that supports this (like the `yt-video-mp3` branch which processes audio).

## Features

*   Download YouTube videos with user-selectable quality (utilizing adaptive streams, which may result in video-only files for higher resolutions).
*   Maintains a history of processed links in `yt_links.txt` to avoid re-downloading.
*   Dockerized for easy setup, portability, and dependency management (includes Python, `pytubefix`, and `ffmpeg`).
*   Persistent storage for downloaded videos and link history via Docker volumes.

### Optimized MP3-Only Conversion (Alternative Branch)

If your primary goal is to quickly convert YouTube videos to MP3 files, an alternative version is available which handles audio processing.

*   **Branch**: `yt-video-mp3`
*   **Purpose**: This branch is optimized for users who predominantly want to extract MP3s. It downloads and processes video and audio streams to produce MP3 files.
*   **To use this version**: Please check out the `yt-video-mp3` branch of this repository for the script that includes MP3 conversion.

## Prerequisites

1.  **Docker**: You need to have Docker installed and running on your system.
    *   Download Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)

2.  **Project Files**:
    *   `youtube_converter.py` (the Python script from the `main` branch for video-only downloads, or from `yt-video-mp3` for MP3 conversion)
    *   `Dockerfile` (to build the Docker image; ensure it includes `ffmpeg` if required by `pytubefix` or for future audio merging)

## Setup: Building the Docker Image

1.  **Clone or Download Files**:
    Ensure you have the `youtube_converter.py` script (from your desired branch) and the `Dockerfile` in the same directory on your local machine.

2.  **Open Your Terminal/Command Prompt**:
    Navigate to the directory where you saved the project files.

    ```
    cd path/to/your/project-directory
    ```

3.  **Build the Docker Image**:
    Run the following command to build the Docker image. This will download the Python base image, install `ffmpeg`, and install the necessary Python library (`pytubefix`).

    ```
    docker build -t youtube-downloader-app .
    ```
    *   `-t youtube-downloader-app`: Tags the image with the name `youtube-downloader-app`. (Note: You might want to use a different tag like `youtube-video-downloader-app` to differentiate if you also build an image for the mp3 branch).
    *   `.`: Specifies that the `Dockerfile` is in the current directory.

    This process might take a few minutes the first time you run it.

## Usage: Running the Application

Once the Docker image is built, you can run the application using the `docker run` command.

1.  **Create Host Directories (Recommended for Persistent Storage)**:
    Create directories on your host machine for downloaded videos and the link history file.

    **In PowerShell (Windows):**
    ```
    New-Item -ItemType Directory -Force -Path ".\my_yt_videos"
    New-Item -ItemType Directory -Force -Path ".\my_yt_data"
    # New-Item -ItemType Directory -Force -Path ".\my_yt_songs" # Kept for consistency if you use the mp3 branch, but not used by main script
    ```

    **In Bash/Zsh (Linux/macOS):**
    ```
    mkdir -p ./my_yt_videos
    mkdir -p ./my_yt_data
    # mkdir -p ./my_yt_songs # Kept for consistency if you use the mp3 branch, but not used by main script
    ```

2.  **Run the Docker Container**:
    The `-v` flag for songs is kept for users who might switch between branches using the same run command, but it's not actively used by the current video-only script.

    **For PowerShell (Windows):**
    ```
    docker run -it --rm `
        -v "${PWD}\my_yt_videos:/app/videos" `
        -v "${PWD}\my_yt_data:/app/data" `
        # -v "${PWD}\my_yt_songs:/app/songs" ` # Optional: if you also use the mp3 branch
        youtube-downloader-app
    ```
    *As a single line:*
    ```
    docker run -it --rm -v "${PWD}\my_yt_videos:/app/videos" -v "${PWD}\my_yt_data:/app/data" youtube-downloader-app
    ```

    **For Bash/Zsh (Linux/macOS):**
    ```
    docker run -it --rm \
        -v "$(pwd)/my_yt_videos:/app/videos" \
        -v "$(pwd)/my_yt_data:/app/data" \
        # -v "$(pwd)/my_yt_songs:/app/songs" \ # Optional: if you also use the mp3 branch
        youtube-downloader-app
    ```

    **Explanation of `docker run` options:**
    *   `-it`: Runs the container in interactive mode.
    *   `--rm`: Automatically removes the container when it exits.
    *   `-v HOST_PATH:CONTAINER_PATH`: Mounts host directories into the container for persistent storage.
        *   `.../my_yt_videos:/app/videos`: For downloaded videos.
        *   `.../my_yt_data:/app/data`: For the `yt_links.txt` history file.
    *   `youtube-downloader-app`: The name of the Docker image.

3.  **Interact with the Script**:
    Once the container is running, you'll see the script's prompt.
    Paste a YouTube video URL and press Enter. You'll be prompted to select video quality.
    The script will download the selected video stream. **Remember, this video may not have audio.**

4.  **Exiting the Script**:
    Type `exit` at the prompt and press Enter.

## Output Files

*   **Downloaded Videos (.mp4)**: Will be saved in the host directory mapped to `/app/videos` (e.g., `my_yt_videos`). **These files are likely video-only, especially for higher resolutions, and may not contain audio.**
*   **Link History (`yt_links.txt`)**: Will be saved in the host directory mapped to `/app/data` (e.g., `my_yt_data`).

## Troubleshooting

*   **HTTP Errors (e.g., 400, 403, 410)**: YouTube's API changes can break downloaders.
    1.  Check internet connection.
    2.  Try a different video.
    3.  Rebuild the Docker image with `--no-cache` to get the latest `pytubefix`: `docker build -t youtube-downloader-app . --no-cache`.
*   **`ModuleNotFoundError`**: Rebuild the Docker image if you've changed dependencies.
*   **`ffmpeg` issues**: While the current script doesn't explicitly use `moviepy` for merging, `ffmpeg` might still be a dependency for `pytubefix` for certain operations or for handling adaptive streams. If you encounter `ffmpeg` related errors during the build or runtime, ensure it's correctly installed in your Docker image.
*   **No Audio in Video**: This is expected for many high-resolution downloads with the current script, as it downloads video-only adaptive streams. For video with audio, consider using the `yt-video-mp3` branch (which handles audio) or modifying the script to download and merge audio.

## Project Files

*   `youtube_converter.py`: The main Python script for downloading videos.
*   `Dockerfile`: Instructions for Docker to build the application image.
*   `README.md`: This documentation file.

## Contact Me

If you have any questions, suggestions, or issues with this project, feel free to reach out or open an issue on the GitHub repository.

*   **Project Maintainer**: Asitha Kanchana Palliyaguru / Asithakanchana1
*   **GitHub Repository**: https://github.com/Asithakanchana1/yt-video-downloader
*   **Issues/Bugs**: Please report any bugs or request features by opening an issue on the [GitHub Issues page for this project](https://github.com/Asithakanchana1/yt-video-downloader/issues).
*   **Email (Optional)**: asitha.contact.me@gmail.com
*   **LinkedIn (Optional)**: [LinkedIn profile](https://linkedin.com/in/asithakanchana)
