import sys
import json
from faster_whisper import download_model
import os

def main():

    models = ['tiny', 'base', 'small', 'medium', 'large']
    download_root = "models"
    for model in models:
        local_files_only = False
        download_model(model, local_files_only=local_files_only, cache_dir=download_root)

if __name__ == '__main__':
    main()