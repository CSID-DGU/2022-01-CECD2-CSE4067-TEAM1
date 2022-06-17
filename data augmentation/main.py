import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas
import pandas as pd
from tqdm import tqdm
import time
import re
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

AUG_MAX = 2
idx = 279


def read_keywords():
    f = open("keywords.txt", 'r')
    ret = f.read()
    ret = ret.replace(' ', ',').replace('\n', ',').replace('\t', ',')
    ret = ret.split(',')

    return list(set(ret))


def substitute_synonym(df, columns, synonyms):
    result = pd.DataFrame(columns=[columns[0], columns[1]])

    for item in tqdm(df.itertuples()):
        # 컬럼명 수정
        eng_msg = item.Q
        kor_msg = item.A

        result = result.append({columns[0]: eng_msg, columns[1]: kor_msg}, ignore_index=True)
        for key, value in synonyms.items():
            for word in value:
                p = re.compile(key, re.I)
                # if key in eng_msg:
                if re.search(p, eng_msg):
                    e = re.sub(p, word, eng_msg)
                    k = re.sub(p, word, kor_msg)
                    # e = eng_msg.replace(key, word)
                    # k = kor_msg.replace(key, word)
                    result = result.append({columns[0]: e, columns[1]: k}, ignore_index=True)

    return result


def augmentation(text, stop_words):
    ret = []

    '''aug = naw.WordEmbsAug(
        model_type='word2vec', model_path='GoogleNews-vectors-negative300.bin',
        action="insert", aug_max=AUG_MAX, stopwords=stop_words)
    augmented_text = aug.augment(text, n=4)
    ret += augmented_text'''

    aug = naw.WordEmbsAug(
        model_type='word2vec', model_path='GoogleNews-vectors-negative300.bin',
        action="substitute", aug_max=AUG_MAX, stopwords=stop_words)
    augmented_text = aug.augment(text, n=4)
    ret += augmented_text

    return ret


def eda(df, columns, stop_words):
    result = pd.DataFrame(columns=[columns[0], columns[1]])
    for item in tqdm(df.itertuples()):
        # 컬럼명 수정
        eng_msg = item.Q
        eng_msg_aug = augmentation(eng_msg, stop_words)
        # 컬럼명 수정
        kor_msg = item.A

        result = result.append({columns[0]: eng_msg, columns[1]: kor_msg}, ignore_index=True)
        for e in eng_msg_aug:
            result = result.append({columns[0]: e, columns[1]: kor_msg}, ignore_index=True)

    return result


if __name__ == '__main__':
    stop_word = read_keywords()
    column = ['Q', 'A']
    df_eda = pd.read_csv("data.csv")

    # df_eda = eda(df_eda, column, stop_word)

    synonym = {'function': ['func', 'fun', 'def', 'fn'],
               'switch': ['when'],
               'else if': ['elif'],
               '==': ['is'],
               "'identifier'": ['tmp', 'a', 'i'],
               "null": ['None', 'undefined', 'nullptr'],
               "modifier": ['qualifier'],
               "qualifier": ['modifier']}

    df_eda = substitute_synonym(df_eda, column, synonym)
    df_eda = eda(df_eda, column, stop_word)
    df_eda.to_excel("data_eda.xlsx", index=False)
