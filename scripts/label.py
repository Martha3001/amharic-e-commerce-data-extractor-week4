import re

products = [
    'Kitchen', 'Hair', 'Tape', 'Power', 'Food', 'Brush', 'Bottle', 'Bath', 'Electric', 'Silicone', 
    'Force', 'Stainless', 'Waterproof', 'Nike', 'Adidas', 'Skechers', 'Reebok', 'Air', 'leather', 
    'Jordan', 'Baby',  'Gel', 'ልብስ', 'ልብሶች', 'Shoes', 'Boots', 'Toothbrush', 'Bag', 'Bags', 'Socks', 
    'Patch', 'Knee', 'Massage', 'Massager', 'Blender', 'Cup', 'Door', 'Table', 'Plate',
    'Towel', 'Coffee', 'Laptop', 'Lamp', 'USB', 'Cap', 'Sticker', 'Foam', 'Water',
    'Bottle', 'Steel', 'Smart', 'Notebook', 'LED', 'Airforce', 'Nike', 'NB',
    'Puma', 'Yeezy', 'Vans', 'loafer', 'Leather', 'suede', 'terrex', 'Goretex', 'Frame',
    'Battery', 'Mop', 'Machine', 'Maker', 'Rack', 'Hand', 'Box', 'Spray', 'Patch', 'Milk',
    'Towel', 'Plate', 'Tool', 'Dry', 'Blender', 'Home', 'Spa', 'Toothbrush', 'Sticker',
    'Patch', 'Kettle', 'Cup', 'Shoes', 'Massager', 'Roller', 'Fan', 'Filter', 'Spa', 'sun',
    'ጁስ', 'ROLEX', 'ኬክ', 'Base', 'Spoon', 'Slicer', 'Grinder', 'pad', 'shoe', 'ጫማ', 'Display',
    'Pan', 'Watches', 'ፍሪጆች', 'Metal', 'መአዛን', 'Feeder', 'Toilet', 'Rubber', 'pairs', 'glasses',
    'mixer', 'blade', 'tempered', 'glass', 'bakeware', 'የመስታዎት', 'ፓትራዎች', 'refrigerators', 'የፍሪጅ',
    'ማስቀመጫ', 'የልብስ', 'ማጠቢያ', 'ላውንደሪዎች', 'protector', 'vegetable', 'cutter', 'cloud', 'chelsea',
    'ማሽን', 'ማፍያ', 'ቡና', 'car', 'ecco', 'zara', 'clips', 'hanger', 'cloth', 'ማስጫ', 'chekich',
    'የልብስም', 'የጫማም', 'ማጠብያ', 'washing', 'ማጠብያ', 'የጫማም', 'የልብስም', 'balenciaga', 'disele'
    ]
locations = [
    'አድራሻ', 'ሜክሲኮ', 'ቦሌ', 'አዲስ', 'አበባ', 'Tera', 'ተራ', 'ሞል', 'ግራንድ', 'አድራሻችን', 'አልሳም', 'ከለላ',
    'መድሀኔአለም', 'ኮሜርስ', 'ጀርባ', 'G07', 'ግራውንድ', 'የሱቅ', 'ቦታ', 'Address',  'ጀሞ', 'መሰናዶ',
    'ፕላዛ', 'አፓርታማ', 'ፊትለፊት', 'አለምነሽ', 'መዚድ', 'ኬኬር', 'ፍሎር', 'አይመን', 'ህንፃ', 'ከ', 
    'ዘፍመሽ', 'መገናኛ', 'ታወር', 'ለይ', 'ድሪም', 'ሀይሎች', 'ጦር', 'fashion', 'ፋሽን'
    ]
price_keywords = ['ዋጋ', 'ብር', 'በ', 'ብር', 'price', 'birr', 'Prices']

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

    # @staticmethod
    def find_price_spans(tokens):
        spans = []
        for i, token in enumerate(tokens):
            if token in price_keywords:
                # Collect following tokens that are numbers or currency
                j = i + 1
                while j < len(tokens) and (tokens[j].isdigit() or tokens[j] == "ብር" or tokens[j] == "birr"):
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

