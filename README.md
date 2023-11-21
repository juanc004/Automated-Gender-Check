# Automated-Gender-Check
## Data_Scrubbing_Script
An automated tool designed to clean textual data by detecting and replacing gender-specific terms, promoting neutrality and reducing potential biases in content.

### Features
- **Automated Scrubbing:** Identifies and replaces gender-specific words based on a predefined list.
- **Word Replacement:** Not only removes but also replaces gender-specific words with neutral alternatives.
- **Fuzzy Matching:** Identifies and flags potential words that might be relevant but aren't clear matches.
- **Feedback Loop:** Allows for continuous refinement based on real-world feedback.
- **Robust Error Handling:** Gracefully handles unexpected situations and provides informative error messages.
- **Detailed Logging:** Provides a clear audit trail for operations and troubleshooting.

### Usage
- **Configuration:** Before running the script, ensure the `ScrubbingCriteria.cfg` file is set up correctly. This file contains the list of words to scrub, their replacements, and the paths for input and output.
- **Running the Script:** Navigate to the directory containing the `DataScrubber.py` script and run it using the command: `python DataScrubber.py`.
- **Feedback Integration:** After manual review, any missed flags or false positives can be added to a feedback file. Use the `FeedbackIntegrator.py` script to integrate this feedback and refine the scrubbing criteria.

### Dependencies
- Python version 3.11
- Required Python libraries: pandas, re, configparser

### Future Enhancements
- Integration with a database for storing and retrieving scrubbing criteria.
- Machine learning-based scrubbing for improved accuracy.
- User interface for easier interaction and configuration.


