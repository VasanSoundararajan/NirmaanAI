# 🗣️ AI Communication Coach

A Streamlit-based application that analyzes speech transcripts to provide feedback on communication skills. It evaluates various criteria such as speech rate, filler words, vocabulary, grammar, and engagement.

## Features

- **Detailed Scoring**: Breakdowns for Salutation, Keywords, Flow, Speech Rate, Grammar, Vocabulary, Filler Words, and Engagement.
- **AI-Powered Analysis**: Uses `sentence-transformers` for semantic matching and `textblob` for sentiment analysis.
- **Grammar Checking**: Integrates `language-tool-python` for grammar and style checking.
- **Visual Feedback**: Interactive progress bars and clear scoring metrics.

## Prerequisites

- Python 3.8+
- Internet connection (for downloading models and accessing the LanguageTool API)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd nirmaan_ai_project
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .env
   # Windows
   .env\Scripts\activate
   # Mac/Linux
   source .env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser at the URL shown (usually `http://localhost:8501`).

3. Paste your speech transcript into the text area.

4. Adjust the audio duration if known.

5. Click **Score My Speech** to get your analysis.

## Project Structure

- `app.py`: Main Streamlit application file handling the UI and user interaction.
- `scorer.py`: Contains the `ScoringEngine` class with logic for analyzing text and calculating scores.

## Dependencies

- `streamlit`
- `textblob`
- `language-tool-python`
- `sentence-transformers`
