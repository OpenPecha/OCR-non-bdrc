
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->

<h3 align="center">Use this repo template for all new Python projects.</h3>

## Project owner(s)

<!-- Link to the repo owners' github profiles -->

- [@ta4tsering](https://github.com/ta4tsering)

## Integrations

<!-- Add any intregrations here or delete `- []()` and write None-->

None
## Docs

### Installation

`pip install -e .`


### Usage
#### OCR Single Book
1. Put the images to be OCRed in its repective folder in the images directory as per its extensions
2. To OCR the images of a single book run `python -m src.OCR_non_bdrc.OCR_books <images_dir_path> <type_of_images>`
#### OCR Multiple Books
1. To OCR images of multiple books, put the images in its respective folder in the images directory as per its extension.
2. To OCR, run `python -m src.OCR_non_bdrc.OCR_books.OCR_multiple_books.py`

<!-- Update the link to the docs -->

Read the docs [here](https://wiki.openpecha.org/#/dev/coding-guidelines).
