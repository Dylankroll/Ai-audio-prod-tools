# Ai-audio-prod-tools
AI Audio Workflow Scripts

This repository contains a small set of Python utilities I’ve used to support AI-assisted audio production workflows, with a focus on narration, voice generation, and post-production organization.

The scripts here are designed to solve practical problems that show up in real production environments: preparing structured inputs for AI voice systems, splitting and validating audio assets, enforcing naming conventions, and organizing outputs so they are easy to edit, QA, and deliver at scale.

These tools were built for internal workflows and personal projects. All examples are generalized and contain no proprietary client data.

What this repository is for:

Preparing and structuring narration assets for AI voice generation

Splitting long recordings into repeatable, labeled segments

Validating file inventories and naming conventions

Batch renaming, conversion, and cleanup of audio files

Organizing generated audio into track-based timelines for post-production

The emphasis is on repeatability, clarity, and quality control rather than one-off scripts.

Included tools (high level):

Audio splitting and segmentation

Scripts to split audio files based on time, index, or mapping files

Designed for workflows where one source file produces many labeled outputs

Track and timeline organization:

track_auto.py
Automates the creation and naming of track structures for AI-generated narration, making it easier to align outputs to scripts, slides, or sections during post-production

Naming and inventory validation:

Tools that compare actual audio outputs against expected mappings

Useful for catching missing files, mis-named assets, or partial generations before delivery

Batch processing and delivery prep:

Utilities for renaming files from CSV or text mappings

Batch format conversion for handoff or platform requirements

Controlled deletion of files using explicit mapping rules

Design approach:

Most scripts in this repo rely on simple external mapping files (.txt or .csv) rather than hard-coded values. This keeps workflows flexible, auditable, and easy to adjust without modifying code.

These tools were written to support time-based service models, where speed matters but mistakes are costly. The goal is to make the “correct” output the default.

Requirements:

Python 3.x

FFmpeg / FFprobe available in PATH (for audio processing scripts)

Some scripts are platform-specific (macOS or Windows), noted in comments

See individual scripts for any additional dependencies.

Notes on safety and scoped:

All scripts operate on local files only

Mapping files included in this repo are examples only

Use caution with deletion utilities and review mappings before running

Why this exists:

I’ve spent years working in audio production environments where AI systems, human editing, and client expectations intersect. These scripts represent the kind of tooling that quietly keeps those workflows reliable: not flashy, but essential.
