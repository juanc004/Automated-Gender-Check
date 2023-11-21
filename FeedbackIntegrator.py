import pandas as pd
import configparser

def validate_feedback_file(feedback_df):
    """
    Validates the structure of the feedback file.
    """
    required_columns = ['Word', 'Action']
    for column in required_columns:
        if column not in feedback_df.columns:
            raise ValueError(f"Missing column '{column}' in feedback file.")
    
    valid_actions = ["add", "remove"]
    for action in feedback_df['Action'].str.lower():
        if action not in valid_actions:
            raise ValueError(f"Invalid action '{action}' in feedback file. Allowed actions are {valid_actions}.")

def integrate_feedback(feedback_file, config_file):
    """
    Integrates feedback from the feedback file into the scrubbing criteria configuration.
    """
    feedback_df = pd.read_csv(feedback_file)
    validate_feedback_file(feedback_df)
    
    config = configparser.ConfigParser()
    config.read(config_file)
    current_words = set(config.get('Criteria', 'gender_words').split(','))
    
    for index, row in feedback_df.iterrows():
        word = row['Word'].strip().lower()
        action = row['Action'].strip().lower()
        
        if action == "add":
            current_words.add(word)
        elif action == "remove":
            current_words.discard(word)  # Using discard to avoid errors if the word isn't present
    
    config.set('Criteria', 'gender_words', ','.join(sorted(current_words)))
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    print("Feedback integrated successfully!")

if __name__ == "__main__":
    FEEDBACK_FILE = 'Feedback.csv'
    CONFIG_FILE = 'ScrubbingCriteria.cfg'
    integrate_feedback(FEEDBACK_FILE, CONFIG_FILE)
