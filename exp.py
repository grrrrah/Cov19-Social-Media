import matplotlib
import sklearn.feature_extraction.text as text
import os
import gensim
import smart_open
import pprint as pp


def get_files(source):
    filenames = sorted([os.path.join(source, filename) for filename in os.listdir(source)])
    return filenames


cnn = get_files(source="news_processed/proccessed cnn")
nyt = get_files(source="news_processed/proccessed nyt")
fox = get_files(source="news_processed/processed fox")


def read_corpus(fname, tokens_only=False):

    with smart_open.open(fname, encoding='iso-8859-1') as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


def return_test_corpus(doc):
    test_corpus_ = []
    doc_test = doc[7:]
    for files in doc_test:
        test_corpus = list(read_corpus(files, tokens_only=True))
        test_corpus_.append(test_corpus)
    flat_list = [item for sublist in test_corpus_ for item in sublist]
    return flat_list


def return_train_corpus(doc):
    doc_train = doc[:7]
    train_corpus_ = []
    for file in doc_train:
        tr_corpus = list(read_corpus(file))
        train_corpus_.append(tr_corpus)
    flat_list = [item for sublist in train_corpus_ for item in sublist]
    return flat_list


cnn_train = return_train_corpus(doc=cnn)
cnn_test = return_test_corpus(doc=cnn)


model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
model.build_vocab(cnn_train)


