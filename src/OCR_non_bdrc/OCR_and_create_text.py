from OCR_books import OCR_book
from create_text import create_repo_for_text
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCR images")
    parser.add_argument(
        'images_dir_path', 
        type=str, 
        help='Path to the images directory'
        )
    parser.add_argument(
        'image_type', 
        type=str,
        help='Type of images'
        )
    parser.add_argument(
        'repo_name', 
        type=str,
        help='repo name'
        )
    args = parser.parse_args()
    OCR_book(args.images_dir_path, args.image_type)
    create_repo_for_text(args.images_dir_path, args.repo_name)