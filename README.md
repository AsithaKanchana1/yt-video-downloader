# YouTube Video Downloader & MP3 Converter (Dockerized)

This project provides a Python script, packaged in a Docker container, to download YouTube videos with user-selectable quality and convert them to MP3 audio files. It uses `pytubefix` for reliable YouTube video downloading (including adaptive streams for higher resolutions) and `moviepy` for video processing and audio extraction/merging.

## Features

* Download YouTube videos with user-selectable quality (utilizing adaptive streams for higher resolutions, requiring video and audio to be merged).
* Convert downloaded videos (or directly process for audio) into MP3 audio files.
* Maintains a history of processed links in `yt_links.txt` to avoid re-downloading/re-converting.
* Dockerized for easy setup, portability, and dependency management (includes Python, `pytubefix`, `moviepy`, and `ffmpeg`).
* Persistent storage for downloaded videos, converted songs, and link history via Docker volumes.

### Optimized MP3-Only Conversion (Alternative Branch)

If your primary goal is to quickly convert YouTube videos to MP3 files and you are not concerned with downloading the video itself, or prefer faster audio extraction from lower-quality video sources, an alternative version is available.

* **Branch**: `yt-video-mp3`
* **Purpose**: This branch is optimized for users who predominantly want to extract MP3s. It may use lower-quality video streams as the source for audio extraction to speed up the process.
* **To use this version**: Please check out the `yt-video-mp3` branch of this repository.

## Prerequisites

1. **Docker**: You need to have Docker installed and running on your system.
   * Download Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)

2. **Project Files**:
    * `youtube_converter.py` (the Python script for the main branch or the `yt-video-mp3` branch)
    * `Dockerfile` (to build the Docker image; ensure it includes `ffmpeg`)

## Setup: Building the Docker Image

1. **Clone or Download Files**:
    Ensure you have the `youtube_converter.py` script (from your desired branch, e.g., `main` or `yt-video-mp3`) and the `Dockerfile` in the same directory on your local machine.

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

    * `-t youtube-converter-app`: Tags the image with the name `youtube-converter-app`.
    * `.`: Specifies that the `Dockerfile` is in the current directory.

    This process might take a few minutes the first time you run it, especially due to `ffmpeg` installation.

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
    * `-it`: Runs the container in interactive mode and allocates a pseudo-TTY, allowing you to interact with the script's input prompts.
    * `--rm`: Automatically removes the container when it exits, keeping your Docker environment clean.
    * `-v HOST_PATH:CONTAINER_PATH`: This is the volume mount flag.
        * `${PWD}\my_yt_videos:/app/videos` (PowerShell) or `$(pwd)/my_yt_videos:/app/videos` (Bash): Maps the `my_yt_videos` directory on your host machine to the `/app/videos` directory inside the container.
        * `${PWD}\my_yt_songs:/app/songs` (PowerShell) or `$(pwd)/my_yt_songs:/app/songs` (Bash): Maps `my_yt_songs` on your host to `/app/songs` inside the container.
        * `${PWD}\my_yt_data:/app/data` (PowerShell) or `$(pwd)/my_yt_data:/app/data` (Bash): Maps `my_yt_data` on your host to `/app/data` inside the container (where `yt_links.txt` is stored).
    * `youtube-converter-app`: The name of the Docker image you built.

3. **Interact with the Script**:
    Once the container is running, you'll see the script's prompt.
    Paste a YouTube video URL and press Enter.
    * If using the main branch version, you'll be prompted to select video quality. Higher quality selections will involve downloading separate video and audio streams, then merging them.
    * The script will download and/or convert the video, saving files to the mounted host directories.

4. **Exiting the Script**:
    Type `exit` at the prompt and press Enter to quit the script. The Docker container will then stop and be automatically removed (due to `--rm`).

## Output Files

* **Downloaded Videos (.mp4)**: Will be saved in the host directory you mapped to `/app/videos` (e.g., `my_yt_videos`). (This may be a temporary merged file or the final video depending on the script version/options chosen).
* **Converted Audio (.mp3)**: Will be saved in the host directory you mapped to `/app/songs` (e.g., `my_yt_songs`).
* **Link History (`yt_links.txt`)**: Will be saved in the host directory you mapped to `/app/data` (e.g., `my_yt_data`). This file stores the URLs of videos that have already been processed. (Note: The original text mentioned `song_yt_links.txt`, ensure your script uses `yt_links.txt` as defined in the script variables).

## Troubleshooting

* **HTTP Errors (e.g., 400, 403, 410)**: YouTube sometimes changes its internal API, which can break downloaders. `pytubefix` is used here as it's generally quicker to adapt to these changes.
    1. Ensure your internet connection is stable.
    2. Try a different video to see if the issue is specific to one link.
    3. Consider rebuilding the Docker image (`docker build -t youtube-converter-app . --no-cache`). The `--no-cache` flag ensures fresh downloads of base images and library installations, which might pull the latest version of `pytubefix` if it has been updated.
* **`ModuleNotFoundError`**: If you see errors about missing modules after modifying the script or `Dockerfile`, ensure you rebuild the Docker image (`docker build ...`) to include the changes.
* **`ffmpeg` errors or issues with merging video/audio**:
    * The `Dockerfile` is responsible for installing `ffmpeg`. If `moviepy` (used for merging adaptive streams or audio extraction) complains about `ffmpeg` not being found or if merging fails, there might have been an issue during the `ffmpeg` installation step when building the image.
    * Check the output of the `docker build` command for any errors related to `apt-get install ffmpeg`.
    * Ensure `ffmpeg` is correctly installed and accessible within the container environment for `moviepy` to use.
*   **File Naming**: Ensure the link history file name in the script (`LINKS_FILE_PATH = os.path.join(BASE_DATA_PATH, "yt_links.txt")`) matches the documentation if you've modified it.

## Project Files

* `youtube_converter.py`: The main Python script for downloading and conversion.
* `Dockerfile`: Instructions for Docker to build the application image, including `ffmpeg`.
* `README.md`: This documentation file.

## Contact Me

If you have any questions, suggestions, or issues with this project, feel free to reach out or open an issue on the GitHub repository.

*   **Project Maintainer**: [Asitha Kanchana Palliyaguru / Asithakanchana1]
*   **GitHub Repository**: [https://github.com/Asithakanchana1]
*   **Issues/Bugs**: Please report any bugs or request features by opening an issue on the [GitHub Issues page for this project](https://github.com/AsithaKanchana1/yt-video-downloader]/issues).
*   **Email (Optional)**: [asitha.contact.me@gmail.com]
*   **LinkedIn (Optional)**: [[LinkedIn profile](https://lk.linkedin.com/in/asithakanchana)]
