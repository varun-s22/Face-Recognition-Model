# Face Recognition Model

This model works on `opencv` module, where it recognizes the face of the person in the image loaded.

## Requirements

Run `poetry install` to get all the required dependencies on your machine
It runs on `opencv`, `numpy` and `os` package.

## Setup

To make your own `trainer.yml` : 

1) Make two directories namely `trained_images` and `untrained_images` (present in `.gitignore`), and then store the data in the `trained_images`.
2) Run `face_train.py` first to get your `trainer.yml`, and then run `face_recognize.py` to get the result
