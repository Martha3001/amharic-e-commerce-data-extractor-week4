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
                "\U0001F680-\U0001F6FF"  # transport & map symbols
                "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                "\U00002700-\U000027BF"  # Dingbats
                "\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)
            normalize_text = emoji_pattern.sub(r'', normalize_text)
            
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
    
    def label_dataframe(df):
        # Example lists and patterns for demonstration; customize for real use
        PRODUCT_WORDS = ["በርገር", "ፓንኬክ", "ስጋ", "ቡና", "ቤት", "ማንኪያ", "ፓስታ",
                        "ዱቄት", "ሻይ", "አላባሹ", "ሻንጣ", "ዳቦ", "ቅመማ", "ልብሶችን",
                        "Stainless", "Steel", "Cookware", "የኪችን", "እቃዎችን", "Water", "Bottle",
                        "የውሀ", "ኮዳ", "BAGS", "GARBAGE", "ከረጢት", "ፕላስቲክ", "የቆሻሻ",
                        "መጣያ", "adidas", "KITCHENWARE", "ሸምቀቆ", "ቦርሳ", "Reebok", "Straightener",
                        "መተኮሻ", "የፀጉር", "Hair", "Brush", "ቦርሳ", "TISHERTS", "መክተፊያ",
                        "መቀስ", "ቢላ", "መጋዝ", "ቢላዎች", "ቤትዎን", "የመኝታ", "ታይት",
                        "ጫማዎች", "ብርቱካን", "የቃሪያ", "መጠጦችን", "የፍራፍሬ", "የሩዝ", 
                        "ልብሶችን"]
        LOCATION_WORDS = ['አድራሻ', 'ድሬዳዋ', 'አሸዋ', 'ሚና', "ተራ", "አበባ", "መገናኛ",
                        'ግራንድ', 'ዘፍመሽ', 'ሞል', 'ጀሞ', "ከለላ", "ህንፃ", "ግራውንድ"]
        PRICE_PATTERN = ['ዋጋ', 'ብር', 'Price']

        # Helper function for entity detection
        def label_token(token, prev_label, product_words, location_words, price_pattern):
            if token in product_words:
                return "B-Product" if prev_label != "B-Product" else "I-Product"
            if token in location_words:
                return "B-LOC" if prev_label != "B-LOC" else "I-LOC"
            if token in price_pattern:
                return "B-PRICE" if prev_label != "B-PRICE" else "I-PRICE"
            
            # If previous token was price and current token is number
            if (prev_label == "B-PRICE" and re.fullmatch(r'\d+(?:[\.,]\d+)?', token )) or prev_label == "I-PRICE":
                return "I-PRICE"
            return "O"

        conll_lines = []
        sample_df = df.dropna(subset=["Cleaned_Message"]).sample(n=min(50, len(df)), random_state=42)
        for _, row in sample_df.iterrows():
            tokens = row["Tokens"]
            prev_label = "O"
            for token in tokens:
                label = label_token(token, prev_label, PRODUCT_WORDS, LOCATION_WORDS, PRICE_PATTERN)
                conll_lines.append(f"{token} {label}")
                prev_label = label if label != "O" else "O"
            conll_lines.append("")  # Blank line between messages

        # Save to plain text file in CoNLL format
        conll_path = '../data/telegram_data_conll.txt'
        with open(conll_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(conll_lines))
        print(f"CoNLL-formatted data saved to {conll_path}")

