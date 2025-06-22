# TikTok Script Generator

This is a simple Streamlit web application that generates TikTok video scripts on any topic using various AI models. It is designed to help content creators quickly draft engaging and well-structured video scripts in Northern Malaysian accent (loghat utara).

## Features

- **Multiple AI Providers**: Supports OpenAI, Gemini, and OpenRouter.
- **Custom Models**: Flexibility to use standard models or specify a custom one.
- **Persistent Settings**: Remembers your API provider, key, and model choice locally in a `settings.json` file.
- **Northern Malaysian Accent**: Generates scripts in colloquial Northern Malaysian accent (loghat utara) with authentic dialect features like "hang" instead of "kau", "dok" instead of "tak", "tok" instead of "saja", etc.
- **Structured Output**: Formats scripts into a clean, four-column markdown table:
    - `Timestamp`
    - `Visual`
    - `Text Overlay`
    - `Voiceover`
- **Variable Length**: Choose between 15, 30, or 60-second video scripts.
- **Script History**: View and manage all previously generated scripts with timestamps and topics.
- **Export to Excel**: Download scripts as Excel files with proper table formatting and auto-adjusted column widths.

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
    - Use the **Export to Excel** button to download the script as an Excel file.

4.  **View and manage history**:
    - Navigate to the **History** tab to view all previously generated scripts.
    - Each script shows the topic, video length, and generation timestamp.
    - Click on any script to expand and view the full content.
    - Use the action buttons to copy, export, or delete individual scripts.
    - Use the **Clear All History** button to remove all saved scripts.

5.  **Export and share**:
    - Excel exports maintain the same table format with auto-adjusted column widths.
    - All generated scripts are automatically saved to your session history. 