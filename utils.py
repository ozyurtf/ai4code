# Importing libraries.
import translators as ts
import textwrap
from html.parser import HTMLParser
from langdetect import detect
import re
from io import StringIO
import json


def detect_language(text_list):
    try:
        joined_texts = ' '.join(text_list)
        detected_language = detect(joined_texts)
    except:
        detected_language = 'N/A'
    return detected_language


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def clean_markdown(text, puncts_to_remove = '!"#$%&\*+-/;<>\\^_`|~'):
    html_s = HTMLStripper()
    html_s.feed(text)

    text_tags_stripped = html_s.get_data()
    text_encoded = text_tags_stripped

    translator = str.maketrans(puncts_to_remove, ' ' * len(puncts_to_remove))

    text_cleaned = text_encoded.translate(translator)
    text_cleaned = re.sub(' +', ' ', text_cleaned)

    return text_cleaned


def extract_shuffled_codes_markdowns(train_or_test, file_id):
    # Importing codes/markdowns data.
    with open(main_path + '{}/{}.json'.format(train_or_test, file_id)) as f:
        data = json.load(f)

    # Extracting shuffled cell ids, cell types, and codes/markdowns, and detecting markdown languages.
    cells_shuffled = list(data['cell_type'].keys())
    cells_shuffled_joined = ' '.join(cells_shuffled)
    cell_types_shuffled = list(data['cell_type'].values())
    codes_markdowns_shuffled = []
    markdowns_shuffled = []
    for k in data['cell_type'].keys():
        cell_type = data['cell_type'][k]
        if cell_type == 'markdown':
            cleaned_markdowns = clean_markdown(data['source'][k])
            codes_markdowns_shuffled.append(cleaned_markdowns)
            markdowns_shuffled.append(cleaned_markdowns)
        else:
            codes = data['source'][k]
            codes_markdowns_shuffled.append(codes)
    markdown_language = detect_language(markdowns_shuffled)

    # Returning the shuffled cell ids, cell types, codes/markdowns, and markdown languages.
    return cells_shuffled_joined, cell_types_shuffled, codes_markdowns_shuffled, markdown_language


def translate(text):
    if len(text)<5000:
        translated_text = ts.google(query_text = text,
                                    from_language = 'auto',
                                    to_language = 'en')
    else:
        text_chunks = textwrap.wrap(text=text,
                                    width=5000,
                                    break_long_words=False,
                                    replace_whitespace=False)
        chunks_translated = []
        for chunk in text_chunks:
            chunk_translated = ts.google(query_text = chunk,
                                         from_language = 'auto',
                                         to_language = 'en')
            chunks_translated.append(chunk_translated)
        translated_text = ' '.join(chunks_translated)
    return translated_text