"""Example: OCR a single PDF file using the OCR-non-bdrc package.

Prerequisites:
    1. Install the package:
           pip install -e /path/to/OCR-non-bdrc

    2. Install poppler (needed by pdf2image to convert PDF pages to images):
           # Ubuntu/Debian
           sudo apt install poppler-utils
           # macOS
           brew install poppler

    3. Set up Google Cloud Vision credentials:
           export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

Usage:
    python ocr_pdf_example.py /path/to/your_file.pdf
    python ocr_pdf_example.py /path/to/your_file.pdf --lang bo
    python ocr_pdf_example.py /path/to/your_file.pdf --lang bo --output result.txt
"""

import argparse
import sys
from pathlib import Path


def ocr_single_pdf(pdf_path: Path, lang: str | None = None, output_path: Path | None = None) -> str:
    """OCR a PDF file and return the extracted text.

    Args:
        pdf_path: Path to the input PDF.
        lang: Optional language hint for Google Vision (e.g. "bo" for Tibetan,
              "en" for English, "zh" for Chinese).
        output_path: If provided, write the text to this file.

    Returns:
        The full extracted text as a string.
    """
    from OCR_non_bdrc.OCR_books import apply_ocr_on_folder, pdf_to_images
    from OCR_non_bdrc.create_text_from_OCR import create_text_from_OCR

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    book_name = pdf_path.stem
    images_dir = Path(f"./data/images/jpeg/{book_name}")
    ocr_dir = Path(f"./data/OCR/{book_name}")
    images_dir.mkdir(parents=True, exist_ok=True)
    ocr_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Converting PDF pages to JPEG → {images_dir}")
    pdf_to_images(pdf_path, images_dir)

    print(f"\n[2/3] Running Google Vision OCR → {ocr_dir}")
    apply_ocr_on_folder(images_dir=images_dir, OCR_dir=ocr_dir, lang=lang)

    print(f"\n[3/3] Extracting text from OCR results …")
    text = create_text_from_OCR(ocr_dir)

    if output_path is None:
        output_path = Path(f"./data/{book_name}.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    print(f"Done! Text saved to {output_path} ({len(text)} characters).")

    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR a PDF using Google Cloud Vision")
    parser.add_argument("pdf", type=Path, help="Path to the PDF file")
    parser.add_argument(
        "--lang",
        default=None,
        help='Language hint for Vision API (e.g. "bo" for Tibetan, "en" for English)',
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output text file path (default: ./data/<pdf_stem>.txt)",
    )
    args = parser.parse_args()

    try:
        ocr_single_pdf(args.pdf, lang=args.lang, output_path=args.output)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
