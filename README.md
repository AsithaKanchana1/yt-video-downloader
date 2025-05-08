# YouTube Video Downloader & MP3 Converter (Dockerized)

This project provides a Python script, packaged in a Docker container, to download YouTube videos and optionally convert them to MP3 audio files. It uses `pytubefix` for reliable YouTube video downloading and `moviepy` for video-to-audio conversion.

## Features

* Download YouTube videos in the highest available progressive resolution.
* Convert downloaded videos into MP3 audio files.
* Maintains a history of processed links in `yt_links.txt` to avoid re-downloading/re-converting.
* Dockerized for easy setup, portability, and dependency management.
* Persistent storage for downloaded videos, converted songs, and link history via Docker volumes.

## Prerequisites

1. **Docker**: You need to have Docker installed and running on your system.
    * Download Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)

2. **Project Files**:
    * `youtube_converter.py` (the Python script)
    * `Dockerfile` (to build the Docker image)

## Setup: Building the Docker Image

1. **Clone or Download Files**:
    Ensure you have the `youtube_converter.py` script and the `Dockerfile` in the same directory on your local machine.

2. **Open Your Terminal/Command Prompt**:
    Navigate to the directory where you saved the project files.

    ```bash
    cd path/to/your/project-directory
    ```

3. **Build the Docker Image**:
    Run the following command to build the Docker image. This will download the Python base image, install `ffmpeg`, and install the necessary Python libraries (`pytubefix`, `moviepy`).
  
    ```bash
    docker build -t youtube-converter-app .
    ```

- `-t youtube-converter-app`: Tags the image with the name `youtube-converter-app`.
-  `.`: Specifies that the `Dockerfile` is in the current directory.

    This process might take a few minutes the first time you run it.

## Usage: Running the Application

Once the Docker image is built, you can run the application using the `docker run` command.

1. **Create Host Directories (Recommended for Persistent Storage)**:
    It's highly recommended to create directories on your host machine where the downloaded videos, converted songs, and the link history file will be stored. This ensures your data persists even if the container is stopped or removed.

    **In PowerShell (Windows):**
 
    ```powershell
    New-Item -ItemType Directory -Force -Path ".\my_yt_videos"
    New-Item -ItemType Directory -Force -Path ".\my_yt_songs"
    New-Item -ItemType Directory -Force -Path ".\my_yt_data"
    ```
 
    **In Bash/Zsh (Linux/macOS):**

    ```bash
    mkdir -p ./my_yt_videos
    mkdir -p ./my_yt_songs
    mkdir -p ./my_yt_data
    ```

    You can name these directories anything you like; just ensure the names match in the `docker run` command.

2. **Run the Docker Container**:

    **For PowerShell (Windows):**
  
    ```powershell
    docker run -it --rm `
        -v "${PWD}\my_yt_videos:/app/videos" `
        -v "${PWD}\my_yt_songs:/app/songs" `
        -v "${PWD}\my_yt_data:/app/data" `
        youtube-converter-app
    ```

    *As a single line:*

    ```powershell
    docker run -it --rm -v "${PWD}\my_yt_videos:/app/videos" -v "${PWD}\my_yt_songs:/app/songs" -v "${PWD}\my_yt_data:/app/data" youtube-converter-app
    ```

    **For Bash/Zsh (Linux/macOS):**
    
    ```bash
    docker run -it --rm \
        -v "$(pwd)/my_yt_videos:/app/videos" \
        -v "$(pwd)/my_yt_songs:/app/songs" \
        -v "$(pwd)/my_yt_data:/app/data" \
        youtube-converter-app
    ```

    **Explanation of `docker run` options:**
    *   `-it`: Runs the container in interactive mode and allocates a pseudo-TTY, allowing you to interact with the script's input prompts.
    *   `--rm`: Automatically removes the container when it exits, keeping your Docker environment clean.
    *   `-v HOST_PATH:CONTAINER_PATH`: This is the volume mount flag.
        *   `${PWD}\my_yt_videos:/app/videos` (PowerShell) or `$(pwd)/my_yt_videos:/app/videos` (Bash): Maps the `my_yt_videos` directory on your host machine to the `/app/videos` directory inside the container (where downloaded MP4s are saved by the script).
        *   `${PWD}\my_yt_songs:/app/songs` (PowerShell) or `$(pwd)/my_yt_songs:/app/songs` (Bash): Maps `my_yt_songs` on your host to `/app/songs` inside the container (where converted MP3s are saved).
        *   `${PWD}\my_yt_data:/app/data` (PowerShell) or `$(pwd)/my_yt_data:/app/data` (Bash): Maps `my_yt_data` on your host to `/app/data` inside the container (where `song_yt_links.txt` is stored).
    *   `youtube-converter-app`: The name of the Docker image you built.

3.  **Interact with the Script**:
    Once the container is running, you'll see the script's prompt:
    ```
     -__________YOUTUBE VIDEO DOWNLOADER & AUDIO CONVERTER (using pytubefix) ___________-

    Enter Link here (or type 'exit' to quit) >>
    ```
    Paste a YouTube video URL and press Enter. The script will download the video, convert it to MP3, and save the files to the mounted host directories.

4.  **Exiting the Script**:
    Type `exit` at the prompt and press Enter to quit the script. The Docker container will then stop and be automatically removed (due to `--rm`).

## Output Files

*   **Downloaded Videos (.mp4)**: Will be saved in the host directory you mapped to `/app/videos` (e.g., `my_yt_videos`).
*   **Converted Audio (.mp3)**: Will be saved in the host directory you mapped to `/app/songs` (e.g., `my_yt_songs`).
*   **Link History (`song_yt_links.txt`)**: Will be saved in the host directory you mapped to `/app/data` (e.g., `my_yt_data`). This file stores the URLs of videos that have already been processed.

## Troubleshooting

*   **HTTP Errors (e.g., 400, 403, 410)**: YouTube sometimes changes its internal API, which can break downloaders. `pytubefix` is used here as it's generally quicker to adapt to these changes than the original `pytube`. If you encounter such errors:
    1.  Ensure your internet connection is stable.
    2.  Try a different video to see if the issue is specific to one link.
    3.  Consider rebuilding the Docker image (`docker build -t youtube-converter-app .`). This can pull the latest version of `pytubefix` (if the library has been updated in `pip` and your `Dockerfile` doesn't pin an older `pytubefix` version) which might contain fixes.
*   **`ModuleNotFoundError`**: If you see errors about missing modules after modifying the script or `Dockerfile`, ensure you rebuild the Docker image (`docker build ...`) to include the changes.
*   **`ffmpeg` errors**: The `Dockerfile` includes `ffmpeg` installation. If `moviepy` complains about `ffmpeg` not being found, there might have been an issue during the `apt-get install ffmpeg` step when building the image. Check the output of the `docker build` command for errors.

## Project Files

*   `youtube_converter.py`: The main Python script for downloading and conversion.
*   `Dockerfile`: Instructions for Docker to build the application image.
*   `README.md`: This documentation file.
