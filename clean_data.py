import spacy
import pandas as pd
import os
import re
import glob


def get_text_without_named_entities(doc, given_name, lang_model):
    global final
    flat_list = []
    nlp = spacy.load(lang_model)
    doc = open(doc, 'r', encoding='utf8')
    doc1 = doc.read()
    document = nlp(doc1)
    entities = [e.string for e in document.ents if 'PERSON' == e.label_]
    item_list = [e for e in entities if e not in ('Donald Trump','Donald Trump ',"Donald Trump's",'Bernie Sanders',
                                                  'Bernie','Sanders','Biden','Joe Biden','Obama','Barack Obama'
                                                  'Trump ', 'Trump','USA','US','SUA','WUHAN','Wuhan','China','American', 'Chinese', 'Americans')]
    item_list = ([s.strip(' ') for s in item_list])
    item_list = ([s.strip("'") for s in item_list])

    final_names = []

    for i in item_list:
        el = i.split(' ')
        final_names.append(el)
        flat_list = [item for sublist in final_names for item in sublist]
    text_no_namedentities = []
    for item in document:
        if item.text not in flat_list:
            text_no_namedentities.append(item.text)
            final = " ".join(text_no_namedentities)
            reg = re.compile(r"^\s+", re.MULTILINE)
            final = reg.sub("", final)
            final = re.sub('[·-]', '', final)
            final = final.replace('  ', ' ')
            reg3 = re.compile(r'^[A-Z][\w]+\s[A-Z][\w]+(?!\S)', re.MULTILINE)
            final = reg3.sub('',final)
            final = re.sub(r"[0-9]+h*", '', final)
            # reg2 = re.compile(r'(?=(.))(?:răspunsuri*|raportează*|place*|acest|comentariu*|editat*'
            #                   r'|Editat*|Ascunde sau*'r'|Îmi*|Răspunde|răspuns)', flags=re.IGNORECASE)
            # final = reg2.sub('',final)
            final = reg.sub("", final)

    with open(given_name, 'w', encoding='utf8') as file:
        file.write(final)


def process_get_new_file(source, lang_model):
    sourcedir = source
    folder = os.listdir(source)
    for doc in folder:

        new_doc_name = doc.replace('.txt', '') + '_new' + '.txt'
        get_text_without_named_entities(doc=source+doc, given_name=new_doc_name, lang_model=lang_model)


# process_get_new_file(source='news/digi24/',lang_model='model-best')
process_get_new_file(source='news/fox news/', lang_model='en_core_web_lg')





