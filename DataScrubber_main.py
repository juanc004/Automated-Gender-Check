import os
import logging
import re
import pandas as pd
import configparser
from collections import Counter
from datetime import datetime

# Set up logging
logging.basicConfig(filename="scrubbing_log.txt", level=logging.INFO)

# Load configuration from the .cfg file
config = configparser.ConfigParser()
config.read('ScrubbingCriteria.cfg')
# Debugging Lines
gender_words = [word.strip() for word in config.get('Criteria', 'gender_words').split(',')]
replacements = {word: config.get('Replacement_Words', word) for word in gender_words}

def validate_config(config):
    """
    Validates the configuration file for required sections and entries.
    """
    required_sections = ['Criteria', 'Paths', 'Replacement_Words']
    for section in required_sections:
        if section not in config.sections():
            raise ValueError(f"Missing section '{section}' in configuration file.")
            
    required_criteria = ['gender_words']
    for criteria in required_criteria:
        if not config.get('Criteria', criteria):
            raise ValueError(f"Missing '{criteria}' in 'Criteria' section of configuration file.")

validate_config(config)

def scrub_and_flag(text):
    """
    Scrubs and flags the provided text based on criteria.
    """
    #Convert the text to a string if it's not already
    text = str(text)
    
    replaced_list = []
    flag = False  # Initialize flag as False (indicating no replacements yet)

    # Replace gender words with their respective replacements and track replaced words
    for word, replacement in replacements.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text, flags=re.IGNORECASE):
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            replaced_list.append(word)
            flag = True # Set flag as True if any replacement occurs
            logging.info(f"Replaced gender word '{word}' with '{replacement}' in: {text}")

    # Remaining logic remains unchanged
    roster_pattern = r'\b\d{2,3}\b'
    flag = 0 if not replaced_list else 1
    uncertain_entries = []

    # Replace roster numbers and update the flag if replacements are made
    if re.search(roster_pattern, text):
        flag = 1
        text = re.sub(roster_pattern, "NN", text)
        logging.info(f"Replaced roster number in: {text}")

    # Identify uncertain entries
    for word in text.split():
        if 2 <= len(word) <= 4 and not word.isalpha():
            uncertain_entries.append(word)

    return text, flag, ', '.join(replaced_list), uncertain_entries

def main():
    input_path = config.get('Paths', 'input_csv_path')
    output_folder = config.get('Paths', 'output_folder_path')

    df = pd.read_csv(input_path)
    if 'Essay' in df.columns:
        results = df['Essay'].apply(scrub_and_flag)
        df['Scrubbed Essay'] = [res[0] for res in results]
        df['Gender Word Flag'] = [res[1] for res in results]
        df['Replaced Words'] = [res[2] for res in results]
        df['Uncertain Entries'] = [res[3] for res in results]

    # Check and scrub the 'Comment' column if it exists
    if 'Comment' in df.columns:
        results = df['Comment'].apply(scrub_and_flag)
        df['Scrubbed Comment'] = [res[0] for res in results]
        df['Gender Word Flag'] = [res[1] for res in results]
        df['Replaced Words'] = [res[2] for res in results]
        df['Uncertain Entries'] = [res[3] for res in results]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Format current date and append it to the output filename
    current_date = datetime.now().strftime("%m-%d-%y")
    output_file_name = os.path.basename(input_path).replace(".csv", f"_scrubbed_{current_date}.csv")
    output_path = os.path.join(output_folder, output_file_name)
    
    df.to_csv(output_path, index=False)

    combined_text = " ".join(df['Scrubbed Essay'])
    words = combined_text.lower().split()
    word_freq = Counter(words)
    common_words = word_freq.most_common(20)
    
    print(common_words)  # Display the most frequent words for review

if __name__ == "__main__":
    main()
