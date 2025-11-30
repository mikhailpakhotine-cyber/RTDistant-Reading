#!/usr/bin/env python3
"""
Distant Reading Analysis Script
Analyzes literary texts for sentiment, style, and thematic content
"""

import re
import json
from collections import Counter
from datetime import datetime
import string


def extract_gutenberg_text(filepath):
    """Extract text content between Project Gutenberg markers"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find start and end markers
    start_pattern = r'\*\*\* START OF.*?EBOOK.*?\*\*\*'
    end_pattern = r'\*\*\* END OF.*?EBOOK.*?\*\*\*'

    start_match = re.search(start_pattern, content, re.IGNORECASE | re.DOTALL)
    end_match = re.search(end_pattern, content, re.IGNORECASE | re.DOTALL)

    if start_match and end_match:
        text = content[start_match.end():end_match.start()]
    else:
        text = content

    return text.strip()


def build_custom_stopwords():
    """Build genre-specific stop word list"""
    # Standard English stop words
    basic_stops = {
        'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
        'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
        'between', 'both', 'but', 'by', 'can', 'could', 'did', 'do', 'does', 'doing',
        'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have',
        'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how',
        'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'might',
        'more', 'most', 'must', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off',
        'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over',
        'own', 'same', 'she', 'should', 'so', 'some', 'such', 'than', 'that', 'the',
        'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this',
        'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we',
        'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will',
        'with', 'would', 'you', 'your', 'yours', 'yourself', 'yourselves'
    }

    # Genre-specific stops for literary/philosophical texts
    literary_stops = {
        'said', 'says', 'one', 'two', 'upon', 'shall', 'may', 'might', 'must',
        'even', 'yet', 'also', 'much', 'many', 'every', 'well', 'still', 'however',
        'therefore', 'thus', 'indeed', 'perhaps', 'though', 'without', 'within',
        'another', 'whether', 'such', 'like', 'seem', 'seemed', 'seems', 'rather',
        'quite', 'almost', 'make', 'made', 'go', 'come', 'came', 'see', 'saw',
        'know', 'knew', 'think', 'thought', 'get', 'got', 'give', 'given', 'took',
        'take', 'us', 'mr', 'chapter'
    }

    return basic_stops | literary_stops


def tokenize_words(text):
    """Convert text to lowercase words, removing punctuation"""
    # Remove punctuation and convert to lowercase
    text = text.lower()
    # Split on whitespace and punctuation
    words = re.findall(r'\b[a-z]+\b', text)
    return words


def tokenize_sentences(text):
    """Split text into sentences"""
    # Simple sentence splitter
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def calculate_word_frequencies(words, stopwords, top_n=50):
    """Calculate word frequencies excluding stopwords"""
    filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    counter = Counter(filtered_words)
    return counter.most_common(top_n)


def analyze_sentiment_simple(text):
    """
    Simple rule-based sentiment analysis
    Note: For production, install vaderSentiment and textblob
    This is a simplified version that works without external dependencies
    """
    text_lower = text.lower()

    # Positive words
    positive_words = {
        'good', 'great', 'excellent', 'wonderful', 'beautiful', 'happy', 'joy',
        'love', 'pleasure', 'delight', 'perfect', 'perfect', 'harmony', 'peace',
        'hope', 'success', 'better', 'best', 'brilliant', 'amazing', 'fantastic',
        'splendid', 'magnificent', 'glorious', 'divine', 'blessed', 'fortunate',
        'prosperous', 'noble', 'admirable', 'wise', 'freedom', 'liberty', 'justice'
    }

    # Negative words
    negative_words = {
        'bad', 'terrible', 'awful', 'horrible', 'sad', 'pain', 'suffer', 'suffering',
        'misery', 'unhappy', 'poor', 'worse', 'worst', 'evil', 'wrong', 'death',
        'fear', 'anxiety', 'despair', 'failure', 'fail', 'lost', 'dark', 'cruel',
        'hate', 'hatred', 'anger', 'bitter', 'terrible', 'dreadful', 'wretched',
        'miserable', 'unfortunate', 'foolish', 'stupid', 'ignorant', 'tyranny'
    }

    words = tokenize_words(text)

    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    total_sentiment_words = pos_count + neg_count

    if total_sentiment_words == 0:
        return {
            'positive': 0.33,
            'negative': 0.33,
            'neutral': 0.34,
            'compound': 0.0,
            'polarity': 0.0,
            'subjectivity': 0.5
        }

    pos_ratio = pos_count / total_sentiment_words if total_sentiment_words > 0 else 0
    neg_ratio = neg_count / total_sentiment_words if total_sentiment_words > 0 else 0

    compound = (pos_count - neg_count) / len(words) if words else 0

    return {
        'positive': round(pos_ratio, 3),
        'negative': round(neg_ratio, 3),
        'neutral': round(1 - pos_ratio - neg_ratio, 3),
        'compound': round(compound, 4),
        'polarity': round((pos_count - neg_count) / total_sentiment_words if total_sentiment_words > 0 else 0, 3),
        'subjectivity': round(total_sentiment_words / len(words) if words else 0, 3)
    }


def find_thematic_keywords(text, sentences):
    """Find keywords related to socialism, utopia, and state with context"""

    themes = {
        'socialism': [
            'socialist', 'socialism', 'collective', 'collectiv', 'labor', 'labour',
            'worker', 'workers', 'class', 'classes', 'equality', 'equal', 'common',
            'communal', 'property', 'ownership', 'wealth', 'distribution', 'capital',
            'capitalist', 'capitalism', 'proletariat', 'bourgeois', 'marx', 'revolution'
        ],
        'utopia': [
            'utopia', 'utopian', 'ideal', 'perfect', 'perfection', 'paradise',
            'eden', 'vision', 'dream', 'imaginary', 'future', 'progress',
            'progressive', 'reform', 'improvement', 'civilization', 'civilized',
            'enlighten', 'enlightenment', 'rational', 'reason'
        ],
        'state': [
            'state', 'government', 'govern', 'law', 'laws', 'authority',
            'authorities', 'power', 'citizen', 'citizens', 'nation', 'national',
            'public', 'administration', 'rule', 'ruler', 'political', 'politics',
            'policy', 'police', 'order', 'control', 'regulation', 'republic'
        ]
    }

    text_lower = text.lower()
    words = tokenize_words(text)
    word_count = len(words)

    results = {}

    for theme_name, keywords in themes.items():
        # Count occurrences
        count = 0
        for word in words:
            for keyword in keywords:
                if keyword in word:
                    count += 1
                    break

        # Find example sentences
        examples = []
        for sentence in sentences[:200]:  # Limit sentence search
            sentence_lower = sentence.lower()
            for keyword in keywords:
                if keyword in sentence_lower and len(examples) < 5:
                    examples.append({
                        'keyword': keyword,
                        'sentence': sentence[:200] + ('...' if len(sentence) > 200 else '')
                    })
                    break

        results[theme_name] = {
            'count': count,
            'density': round(count / word_count * 1000, 2) if word_count > 0 else 0,
            'examples': examples
        }

    return results


def calculate_vocabulary_richness(words):
    """Calculate vocabulary richness metrics"""
    total_words = len(words)
    unique_words = len(set(words))

    # Type-Token Ratio
    ttr = unique_words / total_words if total_words > 0 else 0

    # Average word length
    avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0

    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'type_token_ratio': round(ttr, 4),
        'lexical_diversity': round(ttr * 100, 2),
        'average_word_length': round(avg_word_length, 2)
    }


def calculate_sentence_complexity(sentences):
    """Calculate sentence structure complexity metrics"""
    if not sentences:
        return {
            'total_sentences': 0,
            'average_sentence_length': 0,
            'sentence_length_variance': 0
        }

    sentence_lengths = [len(s.split()) for s in sentences]
    avg_length = sum(sentence_lengths) / len(sentence_lengths)

    # Variance
    variance = sum((x - avg_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)

    return {
        'total_sentences': len(sentences),
        'average_sentence_length': round(avg_length, 2),
        'sentence_length_variance': round(variance, 2),
        'shortest_sentence': min(sentence_lengths),
        'longest_sentence': max(sentence_lengths)
    }


def calculate_readability(words, sentences):
    """Calculate readability scores (Flesch Reading Ease approximation)"""
    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(estimate_syllables(w) for w in words)

    if total_sentences == 0 or total_words == 0:
        return {
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade': 0
        }

    # Flesch Reading Ease
    fre = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

    # Flesch-Kincaid Grade Level
    fkg = 0.39 * (total_words / total_sentences) + 11.8 * (total_syllables / total_words) - 15.59

    return {
        'flesch_reading_ease': round(fre, 2),
        'flesch_kincaid_grade': round(fkg, 2)
    }


def estimate_syllables(word):
    """Estimate syllable count for a word"""
    word = word.lower()
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel

    # Adjust for silent e
    if word.endswith('e'):
        syllable_count -= 1

    # Ensure at least 1 syllable
    if syllable_count == 0:
        syllable_count = 1

    return syllable_count


def analyze_text(filepath, text_id, stopwords):
    """Perform complete analysis on a text"""
    print(f"Analyzing {text_id}...")

    # Extract text
    text = extract_gutenberg_text(filepath)

    # Tokenize
    words = tokenize_words(text)
    sentences = tokenize_sentences(text)

    # Word frequencies
    word_freq = calculate_word_frequencies(words, stopwords, top_n=50)

    # Sentiment
    sentiment = analyze_sentiment_simple(text)

    # Thematic analysis
    themes = find_thematic_keywords(text, sentences)

    # Vocabulary richness
    vocab = calculate_vocabulary_richness(words)

    # Sentence complexity
    sentence_stats = calculate_sentence_complexity(sentences)

    # Readability
    readability = calculate_readability(words, sentences)

    return {
        'id': text_id,
        'basic_stats': {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'character_count': len(text)
        },
        'word_frequencies': [{'word': word, 'count': count} for word, count in word_freq],
        'sentiment': sentiment,
        'thematic_analysis': themes,
        'vocabulary_richness': vocab,
        'sentence_complexity': sentence_stats,
        'readability': readability
    }


def compare_texts(wells_data, dostoyevsky_data):
    """Generate comparative analysis"""
    return {
        'word_count_ratio': round(
            wells_data['basic_stats']['word_count'] / dostoyevsky_data['basic_stats']['word_count'], 2
        ),
        'vocabulary_richness_comparison': {
            'wells_ttr': wells_data['vocabulary_richness']['type_token_ratio'],
            'dostoyevsky_ttr': dostoyevsky_data['vocabulary_richness']['type_token_ratio'],
            'difference': round(
                wells_data['vocabulary_richness']['type_token_ratio'] -
                dostoyevsky_data['vocabulary_richness']['type_token_ratio'], 4
            )
        },
        'sentence_complexity_comparison': {
            'wells_avg': wells_data['sentence_complexity']['average_sentence_length'],
            'dostoyevsky_avg': dostoyevsky_data['sentence_complexity']['average_sentence_length'],
            'difference': round(
                wells_data['sentence_complexity']['average_sentence_length'] -
                dostoyevsky_data['sentence_complexity']['average_sentence_length'], 2
            )
        },
        'sentiment_comparison': {
            'wells_compound': wells_data['sentiment']['compound'],
            'dostoyevsky_compound': dostoyevsky_data['sentiment']['compound'],
            'wells_polarity': wells_data['sentiment']['polarity'],
            'dostoyevsky_polarity': dostoyevsky_data['sentiment']['polarity']
        },
        'readability_comparison': {
            'wells_fre': wells_data['readability']['flesch_reading_ease'],
            'dostoyevsky_fre': dostoyevsky_data['readability']['flesch_reading_ease'],
            'easier_to_read': 'Wells' if wells_data['readability']['flesch_reading_ease'] >
                              dostoyevsky_data['readability']['flesch_reading_ease'] else 'Dostoyevsky'
        }
    }


def main():
    """Main analysis pipeline"""
    print("Starting Distant Reading Analysis...")
    print("=" * 60)

    # Build stop words
    stopwords = build_custom_stopwords()
    print(f"Custom stop words list: {len(stopwords)} words")

    # Save stop words
    with open('stop_words_custom.txt', 'w') as f:
        f.write('\n'.join(sorted(stopwords)))
    print("Saved custom stop words to stop_words_custom.txt")

    # Analyze both texts
    wells_data = analyze_text('WellsModernUtopia.txt', 'wells', stopwords)
    dostoyevsky_data = analyze_text('pg600.txt', 'dostoyevsky', stopwords)

    # Comparison
    comparison = compare_texts(wells_data, dostoyevsky_data)

    # Compile results
    results = {
        'metadata': {
            'analysis_date': datetime.now().isoformat(),
            'texts_analyzed': 2,
            'stop_words_count': len(stopwords)
        },
        'texts': {
            'wells': {
                'title': 'A Modern Utopia',
                'author': 'H. G. Wells',
                **wells_data
            },
            'dostoyevsky': {
                'title': 'Notes from the Underground',
                'author': 'Fyodor Dostoyevsky',
                **dostoyevsky_data
            }
        },
        'comparison': comparison
    }

    # Save to JSON
    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print("Analysis complete!")
    print("Results saved to: analysis_results.json")
    print("\nSummary:")
    print(f"  Wells - {wells_data['basic_stats']['word_count']} words, "
          f"{wells_data['basic_stats']['sentence_count']} sentences")
    print(f"  Dostoyevsky - {dostoyevsky_data['basic_stats']['word_count']} words, "
          f"{dostoyevsky_data['basic_stats']['sentence_count']} sentences")


if __name__ == '__main__':
    main()
