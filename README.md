# entseeker

entseeker is a command-line tool for Named Entity Recognition (NER) and web entity searches in text files. It uses spaCy's NLP capabilities for standard named entities and custom rules for web-related entities.

## Features

- Performs NER using spaCy models
- Identifies web-related entities (URLs, hostnames, IP addresses, etc.)
- Supports multiple spaCy models for different languages
- Allows searching for specific entity types or predefined bundles
- Option to output results to CSV

## Installation

1. Ensure you have Python 3.6 or later installed.

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/entseeker.git
   cd entseeker
   ```

3. Install the required dependency:
   ```
   pip install spacy
   ```

4. Download a spaCy model (the script uses "en_core_web_sm" by default):
   ```
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the script using:

```
python ents.py <input_file> [options]
```

### Options:

- `--model`: Specify a spaCy model (default: en_core_web_sm)
- `--entities`: Specify entity types to search for
- `--types`: Use predefined bundles of entity types
- `--csv`: Output results to a CSV file

### Available Models:

- `en_core_web_sm`: English pipeline (small, 12 MB)
- `en_core_web_md`: English pipeline (medium, 40 MB)
- `en_core_web_lg`: English pipeline (large, 560 MB)
- `en_core_web_trf`: English pipeline with transformer (extra large, 438 MB)
- `xx_ent_wiki_sm`: Multi-language NER model (small, 12 MB)
- `de_core_news_sm`: German pipeline (small, 14 MB)
- `es_core_news_sm`: Spanish pipeline (small, 14 MB)
- `fr_core_news_sm`: French pipeline (small, 14 MB)
- `it_core_news_sm`: Italian pipeline (small, 14 MB)
- `nl_core_news_sm`: Dutch pipeline (small, 13 MB)
- `pt_core_news_sm`: Portuguese pipeline (small, 14 MB)

### Entity Types:

| Type | Description | Example |
|------|-------------|---------|
| PERSON | People, including fictional | John Smith, Harry Potter |
| NORP | Nationalities or religious or political groups | American, Buddhist |
| FAC | Buildings, airports, highways, bridges, etc. | Empire State Building, JFK Airport |
| ORG | Companies, agencies, institutions, etc. | Microsoft, FBI, MIT |
| GPE | Countries, cities, states | France, New York City, Texas |
| LOC | Non-GPE locations, mountain ranges, bodies of water | Alps, Pacific Ocean |
| PRODUCT | Objects, vehicles, foods, etc. (Not services) | iPhone, Boeing 747 |
| EVENT | Named hurricanes, battles, wars, sports events, etc. | World War II, Super Bowl |
| WORK_OF_ART | Titles of books, songs, etc. | "To Kill a Mockingbird" |
| LAW | Named documents made into laws | U.S. Constitution |
| LANGUAGE | Any named language | English, Spanish |
| DATE | Absolute or relative dates or periods | July 4th, last week |
| TIME | Times smaller than a day | 3:30 pm, midnight |
| PERCENT | Percentage, including "%" | 50%, fifty percent |
| MONEY | Monetary values, including unit | $100, 50 euros |
| QUANTITY | Measurements, as of weight or distance | 10 km, 20 pounds |
| ORDINAL | "first", "second", etc. | First, 2nd |
| CARDINAL | Numerals that do not fall under another type | 500, ten |
| URL | Web addresses | https://www.example.com |
| HOSTNAME | Domain names | example.com |
| IP_ADDRESS | IPv4 or IPv6 addresses | 192.168.1.1 |
| PORT | Network port numbers | :8080 |
| PROTOCOL | Network protocols | http://, ftp:// |

### Predefined Type Bundles:

- `people`: PERSON
- `organizations`: ORG, NORP
- `places`: GPE, LOC, FAC
- `things`: PRODUCT, WORK_OF_ART, LAW, LANGUAGE
- `events`: EVENT
- `dates`: DATE, TIME
- `numbers`: PERCENT, MONEY, QUANTITY, ORDINAL, CARDINAL
- `web`: URL, HOSTNAME, IP_ADDRESS, PORT, PROTOCOL

### Examples:

1. Search for all entities in a file:
   ```
   python ents.py input.txt
   ```

2. Search for specific entity types:
   ```
   python ents.py input.txt --entities PERSON ORG
   ```

3. Use predefined entity type bundles:
   ```
   python ents.py input.txt --types people places web
   ```

4. Use a different spaCy model:
   ```
   python ents.py input.txt --model en_core_web_lg
   ```

5. Output results to a CSV file:
   ```
   python ents.py input.txt --csv output.csv
   ```

6. Combine multiple options:
   ```
   python ents.py input.txt --model en_core_web_md --types people organizations web --csv output.csv
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
