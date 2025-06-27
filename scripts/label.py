import re

products = ['Hair', 'Scalp', 'Massager', 'Baby', 'Carrier', 'Core', 
            'Electric', 'computer', 'Stainless', 'humidifier', 'helmet',
             'Silicone', 'battery', 'knee', 'Kitchen', 'ኮምፒውተር', 'socks',
             'i5', 'hd', 'Ram', 'Intel', 'pavilion', 'water', 'Food', 
             'Capacity', 'Power', '8gb', 'Color', 'Tape', 'Steel', 'trouser',
             'storage', 'SSD', 'screen', 'Graphics', 'Battery', 'Water',
             '1tb', 'Double', 'Material', 'Hp', 'Portable', 'hat', 'hanger',
              'Brush', 'design', 'touch', 'Machine', 'inch', 'Screen', 'የሱሪ',
              'DDR4', 'LED', 'Foldable', 'head', 'USB', 'HD', 'RAM', 'ማስቀመጫ',
              'Light', 'steel', 'clean', 'ssd', 'ram', 'power', '4gb', 'kit',
              'GRAPHICS', 'i7', 'Model', 'brand', 'probook', 'Washing', 
              'kitchen', 'Cleaning', 'hdd', 'material','ጫማ','ፈርኒቸር',
              'ቦርሳ','shower', 'cap', 'dish', 'gloves','health','care',
              'milk','powder', 'container', 'feeding', 'bottle','ጥላ','uv',
              'mini','umbrella', 'pocket', 'rack', 'sponge','scrub','body',
              'nail','lamp', 'holder', 'broom', 'potato','chipper','8th',]
locations = ['Bole', 'መሰረት', 'ደፋር', 'ሞል', 'ቢሮ', 'አድራሻ', 'ድሬዳዋ', 'አሸዋ',
              'ሚና', 'ተራ', 'አበባ', 'መገናኛ','ግራንድ', 'ዘፍመሽ', 'ሞል', 'ሁለተኛ',
              'ጀሞ', 'ከለላ', 'ህንፃ', 'ግራውንድ', 'ቦታ', 'ፎቅ', 'ደራርቱ',
              'አደባባይ', 'ዉስጥ', 'እንዳሉ', 'ከታች', 'የራሳችን', 'ሱቅ', 
              'ሱቃችን', 'ያለው', 'ፊት', 'በግራ', 'ጎን', 'ለቡ', 'ጊዮርጊስ',
              'ቤት', 'ሴንተር', 'መስታወትፋብሪካ', 'ሲቲ', 'ሆሊሲቲ', 'አዳማ',
              'ጉርድሾላ', 'ቁ', 'ቁጥር', 'ፊትለፊት', 'ሊፍቱ', 'በኩል','ፒያሳ',
              'ፍሎር', 'ስሪ', 'ኤም','እንዳሉ', 'አዲስ', 'አበባ', 'አዲስአበባ', 
              'ቤተ', 'መዳህኒአለም', 'ክርስቲያን', 'ማራቶን', 'ማእከል','ዋናው', 
              'below', 'መሬት', 'መግቢያ', 'ገበያ', 'ምድር']
price_keywords = ['ዋጋ', 'ብር', 'በ', 'ብር', 'price', 'birr',]

class Label:
    """
    A class for preprocessing Amharic text data, including normalization, tokenization,
    and structuring of metadata and message content.
    """
    def __init__(self):
        Label.initialize()

    # Find entity spans in token list based on dictionary matches (case-insensitive)
    @staticmethod
    def find_entity_spans(tokens, entity_list):
        spans = []
        i = 0
        while i < len(tokens):
            if tokens[i] in [e.lower() for e in entity_list]:
                start = i
                while i < len(tokens) and tokens[i] in [e.lower() for e in entity_list]:
                    i += 1
                spans.append((start, i))
            else:
                i += 1
        return spans

    # Find price spans: looks for price keywords and digits after them
    @staticmethod
    def find_price_spans(tokens):
        spans = []
        for i, token in enumerate(tokens):
            if token in price_keywords:
                # Collect following tokens that are numbers or currency
                j = i + 1
                while j < len(tokens) and (tokens[j].isdigit() or tokens[j] == "ብር"):
                    j += 1
                if j > i + 1:
                    spans.append((i, j))
        return spans

    # Main function to label a list of messages
    @staticmethod
    def label_tokens(tokens):
        labeled_data = []

        # Find spans
        product_spans = Label.find_entity_spans(tokens, products)
        location_spans = Label.find_entity_spans(tokens, locations)
        price_spans = Label.find_price_spans(tokens)
        
        # Initialize tags to O
        tags = ["O"] * len(tokens)
        
        # Mark products
        for start, end in product_spans:
            if tags[start] == "O":
                tags[start] = "B-Product"
                for i in range(start + 1, end):
                    tags[i] = "I-Product"
        
        # Mark locations
        for start, end in location_spans:
            if tags[start] == "O":
                tags[start] = "B-LOC"
                for i in range(start + 1, end):
                    tags[i] = "I-LOC"
                
        
        # Mark prices
        for start, end in price_spans:
            if tags[start] == "O":
                tags[start] = "B-PRICE"
                for i in range(start + 1, end):
                    tags[i] = "I-PRICE"

        # Append token and tag lines
        for token, tag in zip(tokens, tags):
            labeled_data.append(f"{token} {tag}")
        labeled_data.append("")  # blank line to separate messages
        
        return "\n".join(labeled_data)
    
    @staticmethod
    def label_dataframe(df):
        conll_lines = []
        sample_df = df.dropna(subset=["Cleaned_Message"])
        for _, row in sample_df.iterrows():
            tokens = row["Tokens"]
            tokens = [token.lower() for token in tokens]
            label = Label.label_tokens(tokens)
            conll_lines.append(label)

        # Save to plain text file in CoNLL format
        conll_path = '../data/telegram_data_conll.txt'
        with open(conll_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(conll_lines))
        print(f"CoNLL-formatted data saved to {conll_path}")

