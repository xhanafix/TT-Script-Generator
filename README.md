# TikTok Script Generator

This is a simple Streamlit web application that generates TikTok video scripts on any topic using various AI models. It is designed to help content creators quickly draft engaging and well-structured video scripts.

## Features

- **Multiple AI Providers**: Supports OpenAI, Gemini, and OpenRouter.
- **Custom Models**: Flexibility to use standard models or specify a custom one.
- **Persistent Settings**: Remembers your API provider, key, and model choice locally in a `settings.json` file.
- **Multiple Languages**: Generates scripts in colloquial Bahasa Malaysia.
- **Structured Output**: Formats scripts into a clean, four-column markdown table:
    - `Timestamp`
    - `Visual`
    - `Text Overlay`
    - `Voiceover`
- **Variable Length**: Choose between 15, 30, or 60-second video scripts.

## Setup

Follow these steps to get the application running locally.

### 1. Prerequisites

- Python 3.7+
- An API key from OpenAI, Google (for Gemini), or OpenRouter.

### 2. Installation

Clone the repository or download the source files, then install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

1.  **Run the application** from your terminal:

    ```bash
    streamlit run app.py
    ```

2.  **Configure your settings**:
    - Open the **Settings** tab.
    - Select your preferred AI Provider (e.g., OpenAI).
    - Enter your API Key.
    - Choose a model from the list or select "Custom" to enter your own.
    - Click **Save Settings**. Your settings will be saved in a `settings.json` file for future sessions.

3.  **Generate a script**:
    - Navigate to the **Script Generator** tab.
    - Enter a topic for your video.
    - Select the desired video length.
    - Click **Generate Script** and wait for the AI to create your content. 