# Agent Instructions

## Project Purpose

This repository converts a video into a PDF of slides. The process extracts images at regular intervals, removes visually similar images, then combines the retained images into a PDF.

## Verified Workflow

Run commands from the repository root. Always quote paths with double quotes so names containing spaces are supported.

```sh
./extract_diapos.sh "/path/to/video.mp4" "output/video-name"
./remove_dupes.sh "output/video-name"
./merge_as_pdf.sh "output/video-name"
```

The result is `output/video-name.pdf`. Intermediate PNG files remain in `output/video-name/`.

## Script Behavior

- `extract_diapos.sh` uses `ffmpeg` and extracts one image every five seconds (`fps=0.2`).
- `remove_dupes.sh` creates `.venv` when needed, installs the dependencies in `requirements.txt`, then runs `remove_dupes.py --delete`.
- `remove_dupes.py` uses a perceptual hash with `HASH_THRESHOLD = 12`. It actually deletes images identified as duplicates.
- `merge_as_pdf.sh` uses `img2pdf` to combine the remaining PNGs in filename order.

Do not change the extraction frequency or deduplication threshold without an explicit request: these values have been successfully tested with 1920x1080 lecture videos.

## Prerequisites and Diagnostics

The `ffmpeg`, `ffprobe`, and `img2pdf` commands, plus Python 3 with `venv`, must be available. On macOS with Homebrew:

```sh
brew install ffmpeg img2pdf
```

Before a long conversion, check a representative video or confirm the dependencies:

```sh
command -v ffmpeg ffprobe img2pdf python
ffprobe -v error -show_entries format=duration:stream=width,height -of default=noprint_wrappers=1 "/path/to/video.mp4"
```

After conversion, at minimum verify that the PDF exists, has pages, and has a plausible number of remaining PNGs:

```sh
find "output/video-name" -maxdepth 1 -name '*.png' | wc -l
pdfinfo "output/video-name.pdf" | rg 'Pages|Page size|File size'
```

## Precautions

- Process each video in its own output directory so images are not mixed.
- Do not run `remove_dupes.sh` on the only copies of images you want to keep: the script deletes duplicates.
- Do not commit source videos, extracted PNGs, generated PDFs, or `.venv`; they are ignored by `.gitignore`.
- Keep changes limited to the scripts and their documentation. Do not modify input media.