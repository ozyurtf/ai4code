# Importing libraries.
from googletrans import Translator
import textwrap
from html.parser import HTMLParser
import re
from io import StringIO
import json

translator = Translator()


def detect_language(text):
    if type(text) == list:
        detected_language = translator.detect(' '.join(text)).lang
    elif text != '':
        detected_language = translator.detect(text).lang
    elif text == '':
        detected_language = 'N/A'
    return detected_language


def translate_markdown(text):
    if len(text) < 5000 and text != '':
        translated_text = translator.translate(text = text, dest='en').text
    elif len(text) >= 5000:
        text_chunks = textwrap.wrap(text=text,
                                    width=5000,
                                    break_long_words=False,
                                    replace_whitespace=False)
        chunks_translated = []
        for chunk in text_chunks:
            chunk_translated = translator.translate(text = chunk, dest='en').text
            chunks_translated.append(chunk_translated)
        translated_text = ' '.join(chunks_translated)
    elif text == '':
        translated_text = ''
    return translated_text


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

    text_cleaned = text_encoded.translate(str.maketrans(puncts_to_remove, ' ' * len(puncts_to_remove)))
    text_cleaned = re.sub(' +', ' ', text_cleaned)

    return text_cleaned


def extract_shuffled_codes_markdowns(file_id, train_test):
    # Importing codes/markdowns data.
    with open('data/{}/{}.json'.format(train_test, file_id)) as f:
        data = json.load(f)

    # Extracting shuffled cell ids, cell types, and codes/markdowns, and detecting markdown languages.
    cell_orders_shuffled = list(data['cell_type'].keys())
    cell_types_shuffled = list(data['cell_type'].values())

    codes_markdowns_shuffled = []

    for k in data['cell_type'].keys():
        cell_type = data['cell_type'][k]

        if cell_type == 'markdown':
            cleaned_markdown = clean_markdown(data['source'][k])

            # if len(cleaned_markdown) <= 15000 and detect_language(cleaned_markdown) != "en":
            #     cleaned_markdown = translate_markdown(cleaned_markdown)

            codes_markdowns_shuffled.append(cleaned_markdown)

        else:
            codes = data['source'][k]
            codes_markdowns_shuffled.append(codes)

    # Returning the shuffled cell ids, cell types, codes/markdowns, and markdown languages.
    return cell_types_shuffled, cell_orders_shuffled, codes_markdowns_shuffled