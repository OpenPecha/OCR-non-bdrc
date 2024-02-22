from pathlib import Path
import json
import gzip
import statistics
import logging
from fontTools import unicodedata
from openpecha.formatters.ocr.google_vision import GoogleVisionFormatter
from openpecha.formatters.ocr.ocr import OCRFormatter, BBox, UNICODE_CHARCAT_FOR_WIDTH


formatter = OCRFormatter()
remove_non_character_lines = True
remove_rotated_boxes = True


def has_space_attached(symbol):
    if ('property' in symbol and 
            'detectedBreak' in symbol['property'] and 
            'type' in symbol['property']['detectedBreak'] and 
            symbol['property']['detectedBreak']['type'] == "SPACE"):
        return True
    return False


def dict_to_bbox(word):
    confidence = word.get('confidence')
    if 'boundingBox' not in word or 'vertices' not in word['boundingBox']:
        return None
    vertices = word['boundingBox']['vertices']
    bboxinfo = GoogleVisionFormatter.get_bboxinfo_from_vertices(vertices)
    if bboxinfo == None:
        return None
    if remove_rotated_boxes and bboxinfo[4] > 0:
        return None
    return BBox(bboxinfo[0], bboxinfo[1], bboxinfo[2], bboxinfo[3], bboxinfo[4], 
        confidence=confidence)

def get_char_base_bboxes_and_avg_width(response):
    bboxes = []
    widths = []
    if 'fullTextAnnotation' not in response:
        return None, None
    for page in response['fullTextAnnotation']['pages']:
        for block in page['blocks']:
            for paragraph in block['paragraphs']:
                for word in paragraph['words']:
                    bbox = dict_to_bbox(word)
                    if bbox is None:
                        continue
                    cur_word = ""
                    for symbol in word['symbols']:
                        symbolunicat = unicodedata.category(symbol['text'][0])
                        if symbolunicat in UNICODE_CHARCAT_FOR_WIDTH:
                            vertices = symbol['boundingBox']['vertices']
                            width = GoogleVisionFormatter.get_width_of_vertices(vertices)
                            if width is not None and width > 0:
                                widths.append(width)
                        cur_word += symbol['text']
                        if has_space_attached(symbol):
                            cur_word += " "
                    if cur_word:
                        bbox.text = cur_word
                        bbox.language = formatter.get_main_language_code(cur_word)
                        bboxes.append(bbox)
    avg_width = statistics.mean(widths) if widths else None
    logging.debug("average char width: %f", avg_width)
    return bboxes, avg_width


def build_page(bboxes, avg_char_width):
    text = ""
    if not bboxes:
        return text
    sorted_bboxes = formatter.sort_bboxes(bboxes)
    bbox_lines = formatter.get_bbox_lines(sorted_bboxes)
    for bbox_line in bbox_lines:
        if remove_non_character_lines and not formatter.bbox_line_has_characters(bbox_line):
            continue
        if avg_char_width:
            bbox_line = formatter.insert_space_bbox(bbox_line, avg_char_width)
        for bbox in bbox_line:
            text += bbox.text
        text += "\n"
    text += "\n"

    return text

def get_text(ocr_object):
    bboxes, avg_width = get_char_base_bboxes_and_avg_width(response=ocr_object)
    if bboxes == None:
        return
    text = build_page(bboxes, avg_width)
    return text