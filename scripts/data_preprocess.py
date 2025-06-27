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
        Normalize Amharic text by removing diacritics, normalizing unicode, filtering non-Amharic characters,
        and removing size patterns like 'Size #3940#41#42#43', 'Size L#XL', etc.
        Args:
            text (str): The input Amharic text.
        Returns:
            str: The normalized Amharic text.
        """
        if text != "":
            # Remove size patterns like 'Size #3940#41#42#43', 'Size L#XL', etc.
            size_pattern = re.compile(r'Size\s*([#\w]+#?)+', re.IGNORECASE)
            text = size_pattern.sub('', text)
            normalize_text = normalize(text)
            emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F"  # emoticons
                "\U0001F300-\U0001F5FF"  # symbols & pictographs
                "\U0001F680-\U0001F6FF" # transport & map symbols
                "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                "\U00002700-\U000027BF"  # Dingbats
                "\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)
            normalize_text = emoji_pattern.sub(r'', normalize_text)
            punctuation_pattern = re.compile(r"[._!?;:,\-\"'(){}\[\]]")
            normalize_text = punctuation_pattern.sub(r' ', normalize_text)
            return normalize_text.strip()

    @staticmethod
    def tokenize_amharic(text):
        """
        Tokenize Amharic and English text. Uses etnltk's Amharic tokenizer for Amharic segments,
        and regex-based tokenization for English and other scripts, appending all tokens in order.
        Args:
            text (str): The normalized text (Amharic or English or mixed).
        Returns:
            list: List of tokens (words) in the text.
        """
        if not text:
            return []
        tokens = []
        # Split text into runs of Amharic and non-Amharic
        parts = re.findall(r'([\u1200-\u137F]+|[^\u1200-\u137F]+)', text)
        for part in parts:
            if re.search(r'[\u1200-\u137F]', part):
                doc = Amharic(part)
                tokens.extend(doc.words)
            else:
                tokens.extend(re.findall(r"\b\w+\b", part))
        return tokens

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
        df['Cleaned_Message'] = df['Message'].fillna('').apply(lambda x: DataPreprocess.normalize_amharic(x) if x.strip() != '' else '')
        df['Tokens'] = df['Cleaned_Message'].apply(DataPreprocess.tokenize_amharic)
        metadata_cols = ['Channel Title', 'Channel Username', 'ID', 'Date', 'Media Path']
        meta = df[metadata_cols]
        content = df[['Cleaned_Message', 'Tokens']]
        return meta, content, df
