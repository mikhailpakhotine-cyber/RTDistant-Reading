// Global data store
let analysisData = null;
let currentText = 'wells';
let currentTheme = 'socialism';

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    setupNavigation();
    setupThemeTabs();
    displayText(currentText);
});

// Load JSON data
async function loadData() {
    try {
        const response = await fetch('analysis_results.json');
        analysisData = await response.json();

        // Update analysis date
        const date = new Date(analysisData.metadata.analysis_date);
        document.getElementById('analysis-date').textContent = date.toLocaleDateString();

        console.log('Data loaded successfully');
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Error loading analysis data. Please ensure analysis_results.json is in the same directory.');
    }
}

// Setup navigation between texts
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active button
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Show appropriate view
            const textId = btn.dataset.text;

            if (textId === 'comparison') {
                document.getElementById('single-text-view').classList.remove('active');
                document.getElementById('comparison-view').classList.add('active');
                displayComparison();
            } else {
                document.getElementById('comparison-view').classList.remove('active');
                document.getElementById('single-text-view').classList.add('active');
                currentText = textId;
                displayText(textId);
            }
        });
    });
}

// Setup theme tabs
function setupThemeTabs() {
    const themeTabs = document.querySelectorAll('.theme-tab');

    themeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            themeTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentTheme = tab.dataset.theme;
            displayThematicAnalysis(currentText, currentTheme);
        });
    });
}

// Display text analysis
function displayText(textId) {
    const textData = analysisData.texts[textId];

    // Update header
    document.getElementById('text-title').textContent = textData.title;
    document.getElementById('text-author').textContent = `by ${textData.author}`;

    // Basic stats
    document.getElementById('word-count').textContent = textData.basic_stats.word_count.toLocaleString();
    document.getElementById('sentence-count').textContent = textData.basic_stats.sentence_count.toLocaleString();
    document.getElementById('avg-sentence').textContent = textData.sentence_complexity.average_sentence_length;
    document.getElementById('lexical-diversity').textContent = textData.vocabulary_richness.lexical_diversity + '%';

    // Word cloud
    renderWordCloud('wordcloud', textData.word_frequencies);

    // Sentiment
    displaySentiment(textData.sentiment);

    // Thematic analysis
    displayThematicAnalysis(textId, currentTheme);

    // Style analysis
    displayStyleAnalysis(textData);
}

// Render word cloud
function renderWordCloud(containerId, wordFrequencies) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    if (!wordFrequencies || wordFrequencies.length === 0) {
        container.textContent = 'No word frequency data available';
        return;
    }

    // Find max frequency for scaling
    const maxFreq = Math.max(...wordFrequencies.map(w => w.count));
    const minFreq = Math.min(...wordFrequencies.map(w => w.count));

    // Create word elements
    wordFrequencies.forEach((item, index) => {
        const wordSpan = document.createElement('span');
        wordSpan.className = 'word-item';
        wordSpan.textContent = item.word;

        // Scale font size based on frequency (12px to 48px)
        const fontSize = 12 + ((item.count - minFreq) / (maxFreq - minFreq)) * 36;
        wordSpan.style.fontSize = fontSize + 'px';

        // Color gradient based on frequency
        const hue = 240 + (index / wordFrequencies.length) * 60; // Blue to purple
        const saturation = 60 + ((item.count - minFreq) / (maxFreq - minFreq)) * 40;
        wordSpan.style.color = `hsl(${hue}, ${saturation}%, 50%)`;

        // Add tooltip with count
        wordSpan.title = `"${item.word}" appears ${item.count} times`;

        container.appendChild(wordSpan);
    });
}

// Display sentiment analysis
function displaySentiment(sentiment) {
    // Update bars
    const positivePercent = (sentiment.positive * 100).toFixed(1);
    const negativePercent = (sentiment.negative * 100).toFixed(1);
    const neutralPercent = (sentiment.neutral * 100).toFixed(1);

    document.getElementById('sentiment-positive').style.width = positivePercent + '%';
    document.getElementById('sentiment-positive-value').textContent = positivePercent + '%';

    document.getElementById('sentiment-negative').style.width = negativePercent + '%';
    document.getElementById('sentiment-negative-value').textContent = negativePercent + '%';

    document.getElementById('sentiment-neutral').style.width = neutralPercent + '%';
    document.getElementById('sentiment-neutral-value').textContent = neutralPercent + '%';

    // Update metrics
    document.getElementById('polarity').textContent = sentiment.polarity;
    document.getElementById('subjectivity').textContent = sentiment.subjectivity;
}

// Display thematic analysis
function displayThematicAnalysis(textId, theme) {
    const textData = analysisData.texts[textId];
    const themeData = textData.thematic_analysis[theme];

    // Update stats
    document.getElementById('theme-count').textContent = themeData.count;
    document.getElementById('theme-density').textContent = themeData.density;

    // Update examples
    const examplesList = document.getElementById('theme-examples-list');
    examplesList.innerHTML = '';

    if (themeData.examples && themeData.examples.length > 0) {
        themeData.examples.forEach(example => {
            const exampleDiv = document.createElement('div');
            exampleDiv.className = 'example-item';

            const keywordSpan = document.createElement('div');
            keywordSpan.className = 'example-keyword';
            keywordSpan.textContent = example.keyword;

            const sentenceP = document.createElement('p');
            sentenceP.className = 'example-sentence';
            sentenceP.textContent = `"${example.sentence}"`;

            exampleDiv.appendChild(keywordSpan);
            exampleDiv.appendChild(sentenceP);
            examplesList.appendChild(exampleDiv);
        });
    } else {
        examplesList.innerHTML = '<p>No examples found for this theme.</p>';
    }
}

// Display style analysis
function displayStyleAnalysis(textData) {
    // Vocabulary richness
    document.getElementById('ttr').textContent = textData.vocabulary_richness.type_token_ratio;
    document.getElementById('unique-words').textContent = textData.vocabulary_richness.unique_words.toLocaleString();
    document.getElementById('avg-word-length').textContent = textData.vocabulary_richness.average_word_length;

    // Sentence complexity
    document.getElementById('sentence-avg').textContent = textData.sentence_complexity.average_sentence_length;
    document.getElementById('sentence-min').textContent = textData.sentence_complexity.shortest_sentence;
    document.getElementById('sentence-max').textContent = textData.sentence_complexity.longest_sentence;

    // Readability
    document.getElementById('flesch-ease').textContent = textData.readability.flesch_reading_ease;
    document.getElementById('flesch-grade').textContent = textData.readability.flesch_kincaid_grade;
}

// Display comparison view
function displayComparison() {
    const wells = analysisData.texts.wells;
    const dostoyevsky = analysisData.texts.dostoyevsky;
    const comparison = analysisData.comparison;

    // Build comparison table
    const tableBody = document.getElementById('comparison-table-body');
    tableBody.innerHTML = '';

    const metrics = [
        {
            label: 'Word Count',
            wells: wells.basic_stats.word_count.toLocaleString(),
            dostoyevsky: dostoyevsky.basic_stats.word_count.toLocaleString()
        },
        {
            label: 'Sentence Count',
            wells: wells.basic_stats.sentence_count.toLocaleString(),
            dostoyevsky: dostoyevsky.basic_stats.sentence_count.toLocaleString()
        },
        {
            label: 'Lexical Diversity',
            wells: wells.vocabulary_richness.lexical_diversity + '%',
            dostoyevsky: dostoyevsky.vocabulary_richness.lexical_diversity + '%'
        },
        {
            label: 'Type-Token Ratio',
            wells: wells.vocabulary_richness.type_token_ratio,
            dostoyevsky: dostoyevsky.vocabulary_richness.type_token_ratio
        },
        {
            label: 'Avg Sentence Length',
            wells: wells.sentence_complexity.average_sentence_length,
            dostoyevsky: dostoyevsky.sentence_complexity.average_sentence_length
        },
        {
            label: 'Flesch Reading Ease',
            wells: wells.readability.flesch_reading_ease,
            dostoyevsky: dostoyevsky.readability.flesch_reading_ease
        },
        {
            label: 'Sentiment Polarity',
            wells: wells.sentiment.polarity,
            dostoyevsky: dostoyevsky.sentiment.polarity
        },
        {
            label: 'Sentiment (Positive %)',
            wells: (wells.sentiment.positive * 100).toFixed(1) + '%',
            dostoyevsky: (dostoyevsky.sentiment.positive * 100).toFixed(1) + '%'
        },
        {
            label: 'Sentiment (Negative %)',
            wells: (wells.sentiment.negative * 100).toFixed(1) + '%',
            dostoyevsky: (dostoyevsky.sentiment.negative * 100).toFixed(1) + '%'
        }
    ];

    metrics.forEach(metric => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${metric.label}</strong></td>
            <td>${metric.wells}</td>
            <td>${metric.dostoyevsky}</td>
        `;
        tableBody.appendChild(row);
    });

    // Sentiment comparison charts
    displaySentimentChart('wells-sentiment-chart', wells.sentiment);
    displaySentimentChart('dostoyevsky-sentiment-chart', dostoyevsky.sentiment);

    // Word clouds comparison
    renderWordCloud('wells-wordcloud-compare', wells.word_frequencies);
    renderWordCloud('dostoyevsky-wordcloud-compare', dostoyevsky.word_frequencies);
}

// Display sentiment comparison chart
function displaySentimentChart(containerId, sentiment) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    const positivePercent = (sentiment.positive * 100).toFixed(1);
    const negativePercent = (sentiment.negative * 100).toFixed(1);
    const neutralPercent = (sentiment.neutral * 100).toFixed(1);

    container.innerHTML = `
        <div style="margin-bottom: 15px;">
            <div style="margin-bottom: 8px;">
                <strong>Positive:</strong> ${positivePercent}%
            </div>
            <div style="background: #ecf0f1; border-radius: 10px; overflow: hidden;">
                <div style="width: ${positivePercent}%; height: 20px; background: linear-gradient(90deg, #27ae60, #2ecc71);"></div>
            </div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="margin-bottom: 8px;">
                <strong>Negative:</strong> ${negativePercent}%
            </div>
            <div style="background: #ecf0f1; border-radius: 10px; overflow: hidden;">
                <div style="width: ${negativePercent}%; height: 20px; background: linear-gradient(90deg, #c0392b, #e74c3c);"></div>
            </div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="margin-bottom: 8px;">
                <strong>Neutral:</strong> ${neutralPercent}%
            </div>
            <div style="background: #ecf0f1; border-radius: 10px; overflow: hidden;">
                <div style="width: ${neutralPercent}%; height: 20px; background: linear-gradient(90deg, #7f8c8d, #95a5a6);"></div>
            </div>
        </div>
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">
            <div><strong>Polarity:</strong> ${sentiment.polarity}</div>
            <div><strong>Subjectivity:</strong> ${sentiment.subjectivity}</div>
        </div>
    `;
}
