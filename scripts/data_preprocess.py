# Preprocess Amharic text: tokenization, normalization, and structuring
import re
import unicodedata
from etnltk import Amharic
from etnltk.lang.am import normalize

class DataPreprocess:
    """
    A class for preprocessing Amharic text data, including normalization, tokenization,
    and structuring of metadata and message content.
    """
    def __init__(self):
        DataPreprocess.initialize()

    @staticmethod
    def normalize_amharic(text):
        """
        Normalize Amharic text by removing diacritics, normalizing unicode, and filtering non-Amharic characters.
        Args:
            text (str): The input Amharic text.
        Returns:
            str: The normalized Amharic text.
        """
        if text != "":
            normalize_text = normalize(text)
            normalize_text = re.sub(r'[^\u1200-\u137F\s]', '', normalize_text)
            return normalize_text.strip()

    @staticmethod
    def tokenize_amharic(text):
        """
        Tokenize Amharic text using etnltk's Amharic tokenizer.
        Args:
            text (str): The normalized Amharic text.
        Returns:
            list: List of tokens (words) in the text.
        """
        if text != "":
            doc = Amharic(text)
            return doc.words
        return []

    @staticmethod
    def preprocess_dataframe(df):
        """
        Clean and structure the DataFrame by normalizing and tokenizing message content,
        and separating metadata from content.
        Args:
            df (pd.DataFrame): The input DataFrame with a 'Message' column.
        Returns:
            tuple: (metadata DataFrame, content DataFrame, processed DataFrame)
        """
        df['Cleaned_Message'] = df['Message'].fillna('').apply(lambda x: str(DataPreprocess.normalize_amharic(x)))
        df['Tokens'] = df['Cleaned_Message'].apply(DataPreprocess.tokenize_amharic)
        metadata_cols = ['Channel Title', 'Channel Username', 'ID', 'Date', 'Media Path']
        meta = df[metadata_cols]
        content = df[['Cleaned_Message', 'Tokens']]
        return meta, content, df

