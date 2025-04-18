import spacy
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

class TextPreprocessor:
    def __init__(self):
        self.nlp = spacy.load("de_core_news_md")

    def lemmatize_word(self, word: str) -> str:
        if pd.isna(word):
            return word
        doc = self.nlp(word)
        return doc[0].lemma_ if doc and doc[0].lemma_ != word else word

    def lemmatize_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        new_col = f"{column}lemma"
        df[new_col] = df[column].progress_apply(self.lemmatize_word)
        return df