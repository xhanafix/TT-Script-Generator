# TikTok Script Generator

This is a simple Streamlit web application that generates TikTok video scripts on any topic using various AI models. It is designed to help content creators quickly draft engaging and well-structured video scripts in colloquial Bahasa Malaysia (bahasa pasar/Manglish).

## Features

- **Multiple AI Providers**: Supports OpenAI, Gemini, and OpenRouter.
- **Custom Models**: Flexibility to use standard models or specify a custom one.
- **Persistent Settings**: Remembers your API provider, key, and model choice locally in a `settings.json` file.
- **Colloquial Bahasa Malaysia**: Generates scripts in colloquial Bahasa Malaysia (bahasa pasar/Manglish) with authentic conversational features like "kau" or "korang" instead of "anda", "tak" instead of "tidak", "je" instead of "saja", "nak" instead of "hendak", "dah" instead of "sudah", etc.
- **Batch Generation**: Generates 7 unique script variations in a single batch for each topic and video length, helping you choose the best or most creative version.
- **Generation Timing**: Displays how many seconds it took to generate all 7 scripts.
- **Structured Output**: Formats scripts into a clean, four-column markdown table:
    - `Timestamp`
    - `Visual`
    - `Text Overlay`
    - `Voiceover`
- **Export to Excel**: Download scripts as Excel files with proper table formatting and auto-adjusted column widths.
- **Export Voiceover to TXT**: Download just the Voiceover column as a .txt file for easy use in teleprompters.
- **Variable Length**: Choose between 15, 30, or 60-second video scripts.
- **Script History**: View and manage all previously generated scripts with timestamps and topics.

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

3.  **Generate scripts in batch**:
    - Navigate to the **Script Generator** tab.
    - Enter a topic for your video.
    - Select the desired video length.
    - Click **Generate Script**. The app will generate 7 different script variations in a batch.
    - The time taken to generate all scripts will be displayed above the results.
    - For each variation, you can:
        - View the full script in a markdown table.
        - Download the script as an Excel file.
        - Download just the Voiceover column as a .txt file (for teleprompter use).

4.  **View and manage history**:
    - Navigate to the **History** tab to view all previously generated scripts.
    - Each script shows the topic, video length, and generation timestamp.
    - Click on any script to expand and view the full content.
    - Use the action buttons to export or delete individual scripts.
    - Use the **Clear All History** button to remove all saved scripts.

5.  **Export and share**:
    - Excel exports maintain the same table format with auto-adjusted column widths.
    - Voiceover .txt exports are perfect for teleprompter or voiceover use.
    - All generated scripts are automatically saved to your session history. 