# Extract Video Slides to PDF

These scripts periodically extract images from a video, remove visually similar images, and combine the remaining images into a PDF.

## Prerequisites

- `ffmpeg` and `ffprobe`
- `img2pdf`
- Python 3 with the `venv` module

On macOS, install the system tools with Homebrew:

```sh
brew install ffmpeg img2pdf
```

After cloning, make the scripts executable once:

```sh
chmod +x extract_diapos.sh remove_dupes.sh merge_as_pdf.sh
```

## Usage

From the project directory, choose an output directory and replace the paths below with your own:

```sh
./extract_diapos.sh "/path/to/video.mp4" "output/my-video"
./remove_dupes.sh "output/my-video"
./merge_as_pdf.sh "output/my-video"
```

The final file is created at `output/my-video.pdf`.

Paths are quoted so that names containing spaces are supported.

On the first run of `remove_dupes.sh`, a `.venv` virtual environment is created and the Python dependencies in `requirements.txt` are installed automatically.

## How It Works

1. `extract_diapos.sh` extracts one image every five seconds by default.
2. `remove_dupes.sh` compares images with a perceptual hash and removes similar images.
3. `merge_as_pdf.sh` combines the remaining images, in filename order, into a PDF.

Intermediate images remain in the output directory. They can be deleted after the PDF has been checked, if they are no longer needed.

## Settings

- In `extract_diapos.sh`, `fps=0.2` controls the extraction rate. For example, `fps=1` extracts one image per second.
- In `remove_dupes.py`, `HASH_THRESHOLD = 12` controls deduplication sensitivity. A lower value removes only very similar images; a higher value removes more images as similar.

