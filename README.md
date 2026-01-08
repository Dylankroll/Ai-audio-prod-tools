<<<<<<< HEAD
# AI Audio Workflow Scripts

This repository contains a small set of Python utilities I’ve used to support AI-assisted audio production workflows, with a focus on narration, voice generation, and post-production organization.

The scripts here are designed to solve practical problems that show up in real production environments: splitting and validating audio assets, enforcing naming conventions, and organizing outputs so they are easy to edit, QA, and deliver at scale.

These tools were built for internal workflows and personal projects. All examples are generalized and contain no proprietary client data.

## What this repository is for

- Preparing and structuring narration assets for AI voice generation
- Splitting long recordings into repeatable, labeled segments
- Validating file inventories and naming conventions
- Batch renaming, conversion, and cleanup of audio files
- Organizing generated audio into track-based timelines for post-production

The emphasis is on repeatability, clarity, and quality control rather than one-off scripts.

## Included tools (high level)

### Audio splitting and segmentation
- `scripts/audio_split/batch_audio_splitter.py`  
  Batch splitting driven by mapping files for repeatable segmentation and naming.

### Track and timeline organization
- `scripts/track_tools/track_auto.py`  
  Automates creation and naming of track structures for narration workflows (slides, sections, chapters), making alignment and editing faster.

### Naming and inventory validation
- `scripts/qa_naming/namecheckauto.py`  
  Compares expected outputs (from mapping files) against actual files to catch missing assets early.
- `scripts/qa_naming/title_fix.py`  
  Mapping-driven renaming helper for normalizing titles.

### Batch processing and delivery prep
- `scripts/conversion/wav_to_mp3_gui.py`  
  Batch WAV to MP3 helper for delivery formatting.
- `scripts/housekeeping/file_deleter.py`  
  Controlled cleanup utility driven by explicit mapping rules. Review mappings before running.

## Design approach

Most scripts rely on external mapping files (`.txt` or `.csv`) rather than hard-coded values. This keeps workflows flexible, auditable, and easy to adjust without modifying code.

## Requirements

- Python 3.x
- FFmpeg / FFprobe available in PATH (for audio processing scripts)
- Some scripts are platform-specific (macOS or Windows), noted in code comments

## Notes on safety and scope
- All scripts operate on local files only
- Mapping files included here are examples only
- Use caution with cleanup utilities and review mappings before running
>>>>>>> 1687840 (Initial commit: AI audio workflow toolkit)
