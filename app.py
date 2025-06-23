import streamlit as st
import openai
import google.generativeai as genai
import json
import os
import pandas as pd
from datetime import datetime

SETTINGS_FILE = "settings.json"

# Initialize session state for history
if 'script_history' not in st.session_state:
    st.session_state.script_history = []

# --- Settings Functions ---
def load_settings():
    """Loads settings from a JSON file."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {
        "api_provider": "OpenAI",
        "api_key": "",
        "model": "gpt-4"
    }

def save_settings(settings):
    """Saves settings to a JSON file."""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def add_to_history(topic, video_length, script, avatar=None, timestamp=None):
    """Adds a generated script to history."""
    if timestamp is None:
        timestamp = datetime.now()
    
    history_item = {
        'timestamp': timestamp,
        'topic': topic,
        'video_length': video_length,
        'avatar': avatar,  # Store avatar/persona
        'script': script
    }
    st.session_state.script_history.append(history_item)

def create_excel_file(script, topic, video_length):
    """Creates Excel file content from script."""
    try:
        # Parse the markdown table to extract data
        lines = script.strip().split('\n')
        table_data = []
        headers = []
        
        for line in lines:
            if line.startswith('|') and line.endswith('|'):
                # Remove leading/trailing | and split
                cells = [cell.strip() for cell in line[1:-1].split('|')]
                if '---' not in line:  # Skip separator lines
                    if not headers:
                        headers = cells
                    else:
                        table_data.append(cells)
        
        # Create DataFrame
        df = pd.DataFrame(table_data, columns=headers)
        
        # Create Excel file in memory
        output = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
        df.to_excel(output, sheet_name='Script', index=False)
        
        # Auto-adjust column widths
        worksheet = output.sheets['Script']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.close()
        
        # Read the file and return its content
        with open('temp.xlsx', 'rb') as f:
            file_content = f.read()
        
        # Clean up temp file
        os.remove('temp.xlsx')
        
        return file_content
    except Exception as e:
        st.error(f"Error creating Excel file: {e}")
        return None

# Load existing settings and store them in session state
if 'settings_loaded' not in st.session_state:
    settings = load_settings()
    st.session_state.api_provider = settings.get("api_provider", "OpenAI")
    st.session_state.api_key = settings.get("api_key", "")
    st.session_state.model = settings.get("model", "gpt-4")
    st.session_state.settings_loaded = True

# System prompt from user instructions
SYSTEM_PROMPT = """Create a TikTok video script for a specified topic, in colloquial Bahasa Malaysia (bahasa pasar/Manglish). Your audience consists of young, inquisitive users eager to learn. Write the script to explain the topic concisely yet comprehensively, capturing attention initially, maintaining interest, and concluding with a call to action.

- **Tone & Style**: Use a casual, conversational tone in colloquial Bahasa Malaysia (bahasa pasar/Manglish). This includes using "kau" or "korang" instead of formal "anda", "tak" instead of "tidak", "je" instead of "saja", "nak" instead of "hendak", "dah" instead of "sudah", and other colloquial features. Incorporate TikTok trends if relevant. Target three potential video lengths: 15 seconds, 30 seconds, or 60 seconds.
- **Visual Elements**: Include visual cues and overlays to highlight key points. Assume a mix of direct-to-camera and visual overlay parts.

# Steps

1. **Opening**: 
    - Ensure the first few seconds are engaging.
    - Provide a hook to grab attention.
2. **Content**:
    - Maintain a clear, concise explanation of the topic.
    - Keep the content engaging and relevant.
3. **Closing**:
    - Include a call to action, encouraging further engagement.

# Output Format

- **Table Format**: Present the script in a markdown table with four columns: `Timestamp`, `Visual`, `Text Overlay`, and `Voiceover`.
- **Language**: The `Text Overlay` and `Voiceover` columns must be in colloquial Bahasa Malaysia (bahasa pasar/Manglish).
- **Timestamp**: Indicate the start and end time for each segment (e.g., 0:00-0:03).
- **Visual**: Describe the visual elements of the scene.
- **Text Overlay**: Write any text that should appear on the screen (in colloquial Bahasa Malaysia).
- **Voiceover**: Write the spoken words for the script (in colloquial Bahasa Malaysia).

# Colloquial Bahasa Malaysia Features
Use these colloquial features in your script:
- "kau" or "korang" instead of "anda" (you)
- "tak" instead of "tidak" (not)
- "je" instead of "saja" (only/just)
- "nak" instead of "hendak" (want)
- "dah" instead of "sudah" (already)
- "sangat" or "gila" instead of "amat" (very)
- "faham" or "paham" (understand)
- "boleh" or "leh" (can)
- "kat" instead of "di" (at/in)
- "dengan" (with)
- "ni" instead of "ini" (this)
- "tu" instead of "itu" (that)
- "ke" (to)
- "pada" (at/to)
- "macam" instead of "seperti" (like)
- "gila" instead of "sangat" (very/extremely)
- "wey" or "weh" as interjections
- "la" or "lah" as sentence endings

# Example

| Timestamp | Visual | Text Overlay | Voiceover |
| --- | --- | --- | --- |
| 0:00-0:03 | [Muka speaker nampak teruja] | Korang tahu tak? | "Eh korang, korang tahu tak perang paling sekejap dalam sejarah dunia cuma 38 minit je?" |
| 0:04-0:08 | [Gambar-gambar lama Perang Inggeris-Zanzibar] | 27 Ogos 1896 | "Betul wey! Perang Inggeris-Zanzibar tahun 1896. Zanzibar surrender lepas kena bedil dengan kapal British 38 minit je." |
| 0:09-0:15 | [Speaker kembali senyum kat skrin] | #sejarah #faktamenarik | "Nak tahu lagi fakta sejarah gila-gila macam ni? Follow aku!" |

# Notes
- Ensure the script suits a maximum of 60 seconds in length.
- Be mindful of creating an engaging narrative flow.
- Consider using trendy TikTok sound effects or edits where appropriate.
- Always use colloquial Bahasa Malaysia features consistently throughout the script.
- Make sure the language sounds natural and conversational, like how young Malaysians actually speak.
"""

def generate_script(topic, video_length, avatar=None):
    """Generates the TikTok script using the configured AI provider."""
    if not st.session_state.get("api_key"):
        st.error("Please enter your API key in the Settings tab.")
        return None, False
    if not st.session_state.get("model"):
        st.error("Please configure the model in the Settings tab.")
        return None, False

    try:
        provider = st.session_state.api_provider
        api_key = st.session_state.api_key
        model_name = st.session_state.model
        
        user_prompt = f"Create a {video_length}-second TikTok script about {topic}."
        if avatar:
            user_prompt += f"\n\nThe script should be tailored for this product/service avatar/persona: {avatar}"

        if provider == "OpenAI":
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            script = response.choices[0].message.content
            add_to_history(topic, video_length, script, avatar)
            return script, True
        
        elif provider == "OpenRouter":
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                extra_headers={
                    "HTTP-Referer": "http://localhost:8501", 
                    "X-Title": "TikTok Script Generator" 
                }
            )
            script = response.choices[0].message.content
            add_to_history(topic, video_length, script, avatar)
            return script, True

        elif provider == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            full_prompt = f"{SYSTEM_PROMPT}\n\n---\n\n{user_prompt}"
            response = model.generate_content(full_prompt)
            script = response.text
            add_to_history(topic, video_length, script, avatar)
            return script, True

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, False

# --- UI Setup ---
tab_generator, tab_history, tab_settings = st.tabs(["Script Generator", "History", "Settings"])

with tab_generator:
    st.title("TikTok Script Generator")
    topic = st.text_input("Enter the topic for your TikTok video:")
    video_length = st.selectbox("Select video length (in seconds):", [15, 30, 60])
    avatar = st.text_input("Describe your product/service avatar or persona (optional):")  # New input

    if st.button("Generate Script"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating your script..."):
                script, success = generate_script(topic, video_length, avatar)  # Pass avatar
                if script:
                    st.subheader("Your TikTok Script:")
                    st.markdown(script)
                    
                    # Export functionality
                    st.subheader("Export to Excel:")
                    excel_content = create_excel_file(script, topic, video_length)
                    if excel_content:
                        filename = f"tiktok_script_{topic.replace(' ', '_')}_{video_length}s_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        st.download_button(
                            label="📥 Download Excel File",
                            data=excel_content,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

with tab_history:
    st.title("Generated Scripts History")
    
    if not st.session_state.script_history:
        st.info("No scripts generated yet. Generate your first script in the Script Generator tab!")
    else:
        # Show history in reverse chronological order
        for i, item in enumerate(reversed(st.session_state.script_history)):
            with st.expander(f"📝 {item['topic']} ({item['video_length']}s) - {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.markdown(f"**Topic:** {item['topic']}")
                st.markdown(f"**Length:** {item['video_length']} seconds")
                st.markdown(f"**Generated:** {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                if item.get('avatar'):
                    st.markdown(f"**Avatar/Persona:** {item['avatar']}")  # Show avatar if present
                st.markdown("---")
                st.markdown(item['script'])
                
                # Export functionality
                st.subheader("Export to Excel:")
                excel_content = create_excel_file(item['script'], item['topic'], item['video_length'])
                if excel_content:
                    filename = f"tiktok_script_{item['topic'].replace(' ', '_')}_{item['video_length']}s_{item['timestamp'].strftime('%Y%m%d_%H%M%S')}.xlsx"
                    st.download_button(
                        label="📥 Download Excel File",
                        data=excel_content,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_history_{i}"
                    )
                
                # Delete functionality
                if st.button(f"🗑️ Delete Script", key=f"delete_history_{i}"):
                    # Remove from history (accounting for reversed order)
                    actual_index = len(st.session_state.script_history) - 1 - i
                    st.session_state.script_history.pop(actual_index)
                    st.rerun()
        
        # Clear all history button
        if st.button("🗑️ Clear All History"):
            st.session_state.script_history = []
            st.rerun()

with tab_settings:
    st.title("Settings")
    
    # Provider selection
    provider = st.selectbox(
        "Select AI Provider", 
        ["OpenAI", "Gemini", "OpenRouter"], 
        key="selected_api_provider",
        index=["OpenAI", "Gemini", "OpenRouter"].index(st.session_state.get('api_provider', 'OpenAI'))
    )

    # API Key input
    api_key = st.text_input(
        "Enter your API Key:", 
        type="password", 
        key="selected_api_key",
        value=st.session_state.get('api_key', '')
    )

    # Model selection
    if provider == "OpenAI":
        model_options = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "Custom"]
        default_model = st.session_state.get('model', 'gpt-4')
        if default_model not in model_options:
            model_options.append(default_model)
        selected_option = st.selectbox("Select OpenAI Model", model_options, key="selected_model_option", index=model_options.index(default_model if default_model in model_options else "gpt-4"))
        if selected_option == "Custom":
            model = st.text_input("Enter custom model name:", key="selected_model_custom", value=st.session_state.get('model', ''))
        else:
            model = selected_option
            
    elif provider == "Gemini":
        model_options = ["gemini-1.5-pro-latest", "gemini-pro", "Custom"]
        default_model = st.session_state.get('model', 'gemini-pro')
        if default_model not in model_options:
            model_options.append(default_model)
        selected_option = st.selectbox("Select Gemini Model", model_options, key="selected_model_option", index=model_options.index(default_model if default_model in model_options else "gemini-pro"))
        if selected_option == "Custom":
            model = st.text_input("Enter custom model name:", key="selected_model_custom", value=st.session_state.get('model', ''))
        else:
            model = selected_option

    elif provider == "OpenRouter":
        model = st.text_input(
            "Enter model name from OpenRouter (e.g., 'google/gemini-pro'):", 
            key="selected_model_openrouter",
            value=st.session_state.get('model', '')
        )

    if st.button("Save Settings"):
        st.session_state.api_provider = provider
        st.session_state.api_key = api_key
        st.session_state.model = model
        
        settings_to_save = {
            "api_provider": provider,
            "api_key": api_key,
            "model": model
        }
        save_settings(settings_to_save)
        st.success("Settings saved successfully!")

    st.info("Your settings are saved locally in settings.json and will be loaded next time.") 