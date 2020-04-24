import nltk
import spacy
import pandas as pd
import os

nlp = spacy.load("en_core_web_sm")


def turn_into_df(document):
    document_name = document.replace('.txt','')
    df = pd.read_csv(sourcedir + '/' + document, delimiter='\n', encoding='utf-8', header=None)
    df.columns = [document_name]
    return df


df_list = []
sourcedir = 'proccessed nyt'
folder = os.listdir(sourcedir)
for i in folder:
    b = turn_into_df(document=i)
    df_list.append(b)


for df in df_list:
    for item in df:
        print(df[item])