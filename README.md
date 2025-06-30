# **EthioMart: Amharic NER for Telegram E-Commerce**

## **Project Overview**
This project focuses on developing a **Named Entity Recognition (NER) system** for Amharic text extracted from Ethiopian Telegram e-commerce channels. The goal is to identify key business entities (products, prices, locations) to populate **EthioMart's** centralized database.

### **Key Features**
- 📥 **Data Ingestion**: Scrapes Telegram channels for text and images
- ✨ **Text Preprocessing**: Normalizes and tokenizes Amharic text
- 🏷️ **Entity Labeling**: Converts raw text into CoNLL format for NER
- 🤖 **Model Fine-Tuning**: Adapts multilingual LLMs (XLM-Roberta, mBERT) for Amharic NER
- 📊 **Vendor Analytics**: Generates scorecard to evaluate vendor performance

## **Repository Structure**
```
├── data/
│ ├── photos/ # Raw datasets (original data files)
│ ├── telegram_data_conll.txt # Labeled dataset
│ ├── telegram_data_processed.csv # Processed datasets
│ └── telegram_data.csv # Raw datasets
├── notebooks/
│ ├── __init__.py 
│ ├── data_preprocessig.ipynb # Notebook for preprocess and labeling
│ ├── model.ipynb # Notebook for model
│ └── scorecard.ipynb # Notebook for score card
├── scripts/
│ ├── __init__.py 
│ ├── .env # environment variables
│ ├── data_ingestion.py # Script for extraction 
│ ├── label.py # Script for labeling
│ └── data_preprocess.py # Script for preprocess
├── tests/
│ ├── __init__.py 
│ └── test_data_preprocess.py # Test for preprocess and labeling
├── .gitignore # Specifies files to ignore in Git
├── README.md # This file
└── requirements.txt # Python dependencies
```

## **Setup**
1. Clone: `git clone https://github.com/Martha3001/amharic-e-commerce-data-extractor-week4.git`
2. Create venv: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows)
4. Install: `pip install -r requirements.txt`
5. Configure Telegram API
   - Obtain API_ID and API_HASH from Telegram Developer Portal.
   - Add credentials to .env:

    ```bash
    api_id = YOUR_API_ID
    api_hash = YOUR_API_HASH
    phone = YOUR_PHONE_NUMBER
    ```

## **Results**

### **Model Performance**
| Model          | F1-Score | Accuracy |
|----------------|----------|----------|
| XLM-Roberta    | 0.973    | 0.994    |
| mBERT          | 0.948    | 0.989    |

### **Top Vendor (Example)**
| Channel                     | Lending Score | Avg Price (ETB) |
|-----------------------------|---------------|-----------------|
| @ethio_brand_collection     | 19,976        | 3,378           |

