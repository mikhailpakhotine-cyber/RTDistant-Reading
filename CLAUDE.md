# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RTDistant-Reading is a text analysis project that performs distant reading, sentiment analysis, and style comparison on literary texts. The repository currently contains two Project Gutenberg texts:

- `WellsModernUtopia.txt` - "A Modern Utopia" by H.G. Wells (Project Gutenberg #6424)
- `pg600.txt` - "Notes from the Underground" by Fyodor Dostoyevsky (Project Gutenberg #600)

## Project Goals

The project aims to:
1. Conduct distant reading analysis on the texts
2. Perform sentiment analysis on each text
3. Compare writing styles between texts
4. Generate JSON output with all analysis results
5. Provide an interactive HTML/CSS/JavaScript interface for exploring the analysis, including:
   - Navigation by text
   - Word clouds
   - Analysis visualization
   - Text comparison functionality

## Architecture

The project will consist of:
- **Analysis Module**: Python-based text processing and NLP analysis (sentiment, word frequency, style metrics)
- **Data Layer**: JSON files containing analysis results
- **Web Interface**: Static HTML/CSS/JavaScript application for interactive exploration
- **Text Data**: Raw Project Gutenberg text files

## Development Commands

Since this is a Python-based text analysis project, typical commands will include:

```bash
# Run analysis
python analyze.py

# Run specific analysis on a single text
python analyze.py --file WellsModernUtopia.txt

# Generate visualization data
python generate_wordcloud.py

# Start local web server for the interface
python -m http.server 8000
```

## Text Processing Notes

- Project Gutenberg texts include front matter and license text that should be excluded from analysis
- Look for "*** START OF THE PROJECT GUTENBERG EBOOK" and "*** END OF THE PROJECT GUTENBERG EBOOK" markers
- Text encoding is UTF-8 (note the BOM character at start of files)
