# Chat Analyzer

Chat Analyzer is a powerful data analysis tool designed to extract meaningful insights from chat history files. This application supports different time formats, processes messages efficiently, and provides comprehensive statistics on chat activities. Users can analyze metrics such as total messages, word counts, common words, and emoji usage, among others.

# Features

* User-Based Chat Analysis: Analyze chat statistics based on individual users or overall conversation trends.
* Word Cloud Visualization: Generate a word cloud to showcase frequently used words.
* Common Words Analysis: Identify the most common words exchanged in the chat, offering a snapshot of conversational themes.
* Emoji Analysis: Break down emoji usage to see which are used the most and by whom.
* Data Processing Options: Supports 12-hour, 24-hour, and customizable time formats to process chat logs.

  # Getting Started

* Python 3.7 or later
* Streamlit (pip install streamlit)
* Additional libraries: pandas, numpy, matplotlib, nltk, wordcloud, emoji, seaborn
* Machine Learning

# Installation

- git clone https://github.com/yourusername/Chat-Analyzer.git
cd Chat-Analyzer

- pip install -r requirements.txt

- streamlit run app.py

# Usage

* Launch the application and upload your chat file.
* Choose the time format used in the chat file (12-hour, 24-hour, or custom).
* Select a specific user or analyze the overall chat.
* Click "Show Analysis" to view detailed insights.

# File Structure

* app.py: Main application script for the Chat Analyzer.
* preprocess.py: Handles chat data preprocessing.
* stats.py: Contains functions for generating statistics and visualizations.



