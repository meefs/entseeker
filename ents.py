#!/usr/bin/env python3
# Filename: comprehensive_ner_search.py

import spacy
from spacy.matcher import Matcher
import sys
import os
import argparse
import csv

def get_common_models():
    return [
        {
            "name": "en_core_web_sm",
            "size": "Small (12 MB)",
            "description": "English pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "en_core_web_md",
            "size": "Medium (40 MB)",
            "description": "English pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "en_core_web_lg",
            "size": "Large (560 MB)",
            "description": "English pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "en_core_web_trf",
            "size": "Extra Large (438 MB)",
            "description": "English pipeline with transformer. Requires spacy-transformers package. Components: tok,transformer,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "xx_ent_wiki_sm",
            "size": "Small (12 MB)",
            "description": "Multi-language NER model. Identifies LOC,MISC,ORG,PER entities."
        },
        {
            "name": "de_core_news_sm",
            "size": "Small (14 MB)",
            "description": "German pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "es_core_news_sm",
            "size": "Small (14 MB)",
            "description": "Spanish pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "fr_core_news_sm",
            "size": "Small (14 MB)",
            "description": "French pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "it_core_news_sm",
            "size": "Small (14 MB)",
            "description": "Italian pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "nl_core_news_sm",
            "size": "Small (13 MB)",
            "description": "Dutch pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        },
        {
            "name": "pt_core_news_sm",
            "size": "Small (14 MB)",
            "description": "Portuguese pipeline optimized for CPU. Components: tok,tagger,parser,ner,attribute_ruler,lemmatizer."
        }
    ]

def get_entity_types():
    return [
        "PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT",
        "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY",
        "QUANTITY", "ORDINAL", "CARDINAL",
        # Web entities
        "URL", "HOSTNAME", "IP_ADDRESS", "PORT", "PROTOCOL"
    ]

def get_entity_type_bundles():
    return {
        "people": ["PERSON"],
        "organizations": ["ORG", "NORP"],
        "places": ["GPE", "LOC", "FAC"],
        "things": ["PRODUCT", "WORK_OF_ART", "LAW", "LANGUAGE"],
        "events": ["EVENT"],
        "dates": ["DATE", "TIME"],
        "numbers": ["PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"],
        "web": ["URL", "HOSTNAME", "IP_ADDRESS", "PORT", "PROTOCOL"]
    }

def download_model(model_name):
    print(f"Downloading spaCy model: {model_name}")
    spacy.cli.download(model_name)
    print("Model downloaded successfully.")

def add_web_entities(nlp):
    matcher = Matcher(nlp.vocab)
    
    # URL pattern
    url_pattern = [{"LIKE_URL": True}]
    matcher.add("URL", [url_pattern])
    
    # Updated Hostname pattern (FQDN only)
    hostname_pattern = [{"TEXT": {"REGEX": r"(?<![:/\w])(?:(?:www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})(?![:/\w])"}}]
    matcher.add("HOSTNAME", [hostname_pattern])
    
    # IP Address pattern
    ip_pattern = [{"TEXT": {"REGEX": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"}}]
    matcher.add("IP_ADDRESS", [ip_pattern])
    
    # Port pattern (including the colon)
    port_pattern = [{"TEXT": {"REGEX": r":\d{1,5}"}}]
    matcher.add("PORT", [port_pattern])
    
    # Protocol pattern
    protocol_pattern = [{"LOWER": {"IN": ["http", "https", "ftp", "sftp", "ssh", "rtmp"]}}, {"TEXT": "://"}]
    matcher.add("PROTOCOL", [protocol_pattern])
    
    return matcher

def search_entities(file_path, entity_types, model_name):
    if not spacy.util.is_package(model_name):
        download_model(model_name)
    
    nlp = spacy.load(model_name)
    web_matcher = add_web_entities(nlp)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    doc = nlp(text)
    
    results = []
    
    # First, add standard NER results
    for ent in doc.ents:
        if entity_types is None or ent.label_ in entity_types:
            results.append((ent.text, ent.label_, ent.start_char, ent.end_char, 'ner'))
    
    # Then, add web entity matches
    matches = web_matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]
        if entity_types is None or label in entity_types:
            results.append((span.text, label, span.start_char, span.end_char, 'web'))
    
    # Sort results by start position
    results.sort(key=lambda x: x[2])
    
    return results

def write_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Text', 'Label', 'Start', 'End', 'Type'])
        for result in results:
            writer.writerow(result)

def main():
    models = get_common_models()
    entity_types = get_entity_types()
    entity_type_bundles = get_entity_type_bundles()

    parser = argparse.ArgumentParser(description="Named Entity Recognition and Web Entity search tool", 
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("file_path", help="Path to the input text file")
    parser.add_argument("--model", default="en_core_web_sm", help="Specify a spaCy model to use")
    parser.add_argument("--entities", nargs="+", metavar="ENTITY_TYPE", help="Entity types to search for")
    parser.add_argument("--types", nargs="+", choices=entity_type_bundles.keys(), help="Bundled entity types to search for")
    parser.add_argument("--csv", help="Output results to a CSV file")
    
    # Add detailed model information to the help text
    parser.epilog = "Common spaCy models:\n"
    for model in models:
        parser.epilog += f"{model['name']} - {model['size']}\n"
        parser.epilog += f"  {model['description']}\n\n"
    
    parser.epilog += "Available entity types:\n"
    parser.epilog += ", ".join(entity_types) + "\n\n"
    parser.epilog += "Available entity type bundles:\n"
    for bundle, types in entity_type_bundles.items():
        parser.epilog += f"{bundle}: {', '.join(types)}\n"
    parser.epilog += "\nNote: Available entity types may vary depending on the model used."

    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"Error: File '{args.file_path}' not found.")
        sys.exit(1)

    selected_entity_types = set()
    if args.entities:
        selected_entity_types.update(args.entities)
    if args.types:
        for bundle in args.types:
            selected_entity_types.update(entity_type_bundles[bundle])

    results = search_entities(args.file_path, selected_entity_types if selected_entity_types else None, args.model)
    
    if args.csv:
        write_csv(results, args.csv)
        print(f"Results written to {args.csv}")
    else:
        if selected_entity_types:
            print(f"Entities of types {', '.join(selected_entity_types)}:")
        else:
            print("All entities found:")
        
        for result in results:
            print(f"{result[0]} ({result[1]}: {result[2]}:{result[3]}) [Type: {result[4]}]")

if __name__ == "__main__":
    main()
