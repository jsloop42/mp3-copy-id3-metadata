"""
Author: Jaseem V V
Date: Sat 20 Jan 2024
Version: 1.0

A script to copy mp3 ID3 tags from source mp3 to destination mp3 for all files present in the source to the
corresponding files in the destination.

To run:
% python3 mp3-copy-meta.py ~/Temp/src ~/Temp/dst
"""

__version__ = "1.0"

import eyed3
import os
import sys


def copy_id3_tags(src_path, dst_path):
    source = eyed3.load(src_path)
    destination = eyed3.load(dst_path)
    if source is not None and source.tag is not None:
        if destination is not None:
            if destination.tag is None:
                destination.initTag()
            destination.tag.frame_set = source.tag.frame_set
            destination.tag.save()
            print(f"Metadata copied for {os.path.basename(dst_path)}.")
        else:
            print("Error loading destination file")
    else:
        print('Source file not found or there is no metadata in source')


def find_and_copy_id3_tags(src_folder, dst_folder):
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(dst_folder, file)
            if os.path.exists(destination_path):
                copy_id3_tags(source_path, destination_path)


if __name__ == "__main__":
    # Check if both source and destination folders are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 mp3-copy-meta.py source-folder destination-folder")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]

    # Check if the provided folders exist
    if not os.path.exists(source_folder) or not os.path.exists(destination_folder):
        print("Source or destination folder does not exist.")
        sys.exit(1)

    find_and_copy_id3_tags(source_folder, destination_folder)
