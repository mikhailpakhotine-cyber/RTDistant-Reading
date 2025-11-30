# RTDistant-Reading

A distant reading analysis project for comparing literary texts using natural language processing and visualization techniques.

## Overview

This project performs comprehensive text analysis on two classic works:
- **"A Modern Utopia"** by H.G. Wells
- **"Notes from the Underground"** by Fyodor Dostoyevsky

The analysis includes:
- Word frequency analysis with interactive word clouds
- Sentiment analysis (positive/negative/neutral)
- Thematic analysis (socialism, utopia, state-related language)
- Style comparison (vocabulary richness, sentence complexity)
- Readability metrics

## Files

- `analyze.py` - Python script that performs all text analysis
- `analysis_results.json` - Generated analysis data in JSON format
- `stop_words_custom.txt` - Custom stop words list for the literary genre
- `index.html` - Interactive web interface
- `style.css` - Styling for the web interface
- `app.js` - JavaScript for interactive features
- `WellsModernUtopia.txt` - Source text (H.G. Wells)
- `pg600.txt` - Source text (Dostoyevsky)

## Usage

### Running the Analysis

```bash
python3 analyze.py
```

This will:
1. Extract text content (excluding Project Gutenberg front/back matter)
2. Build a custom stop words list
3. Analyze both texts for sentiment, themes, and style
4. Generate `analysis_results.json` with all findings

### Viewing the Results

Open `index.html` in a web browser, or serve it with a local HTTP server:

```bash
python3 -m http.server 8000
```

Then navigate to `http://localhost:8000` in your browser.

### Web Interface Features

- **Text Navigation**: Switch between Wells and Dostoyevsky analysis views
- **Word Clouds**: Interactive visualization of top 50 words (sized by frequency)
- **Sentiment Analysis**: Visual breakdown of positive/negative/neutral sentiment
- **Thematic Analysis**: Keyword analysis for socialism, utopia, and state-related terms with example sentences in context
- **Style Metrics**: Vocabulary richness, sentence complexity, and readability scores
- **Comparison View**: Side-by-side comparison of all metrics between both texts

## Analysis Details

### Sentiment Analysis
Uses rule-based approach with custom positive/negative word dictionaries to calculate:
- Positive/negative/neutral percentages
- Polarity score (-1 to 1)
- Subjectivity score (0 to 1)

### Thematic Keywords
Identifies and counts occurrences of terms related to:
- **Socialism**: collective, labor, worker, class, equality, etc.
- **Utopia**: ideal, perfect, paradise, vision, progress, etc.
- **State**: government, law, authority, citizen, nation, etc.

Displays density (per 1000 words) and example sentences in context.

### Style Analysis
- **Vocabulary Richness**: Type-Token Ratio, lexical diversity, unique word count
- **Sentence Complexity**: Average sentence length, variance, min/max
- **Readability**: Flesch Reading Ease and Flesch-Kincaid Grade Level

## Requirements

- Python 3.x (no external libraries required - uses standard library only)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## License

The source texts are from Project Gutenberg and are in the public domain.
Analysis code is provided as-is for educational purposes.
