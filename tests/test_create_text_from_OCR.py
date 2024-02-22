from pathlib import Path
from OCR_non_bdrc.create_text_from_OCR import create_text_from_OCR


def test_create_text_from_OCR():
    OCR_path = Path("./tests/data/OCR/༄༅།།རྗེ་བཙུན་སྒྲོལ་མའི་བསྟོད་པ།")
    text = create_text_from_OCR(OCR_path)
    expected_text = Path(f"./tests/data/expected_text.txt").read_text(encoding="utf-8")
    assert text == expected_text


if __name__ == "__main__":
    test_create_text_from_OCR()