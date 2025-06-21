import streamlit as st
import openai
import google.generativeai as genai
import json
import os

SETTINGS_FILE = "settings.json"

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

# Load existing settings and store them in session state
if 'settings_loaded' not in st.session_state:
    settings = load_settings()
    st.session_state.api_provider = settings.get("api_provider", "OpenAI")
    st.session_state.api_key = settings.get("api_key", "")
    st.session_state.model = settings.get("model", "gpt-4")
    st.session_state.settings_loaded = True

# System prompt from user instructions
SYSTEM_PROMPT = """Create a TikTok video script for a specified topic, in colloquial Bahasa Malaysia. Your audience consists of young, inquisitive users eager to learn. Write the script to explain the topic concisely yet comprehensively, capturing attention initially, maintaining interest, and concluding with a call to action.

- **Tone & Style**: Use a casual, conversational tone in colloquial Bahasa Malaysia (Manglish/bahasa pasar). Incorporate TikTok trends if relevant. Target three potential video lengths: 15 seconds, 30 seconds, or 60 seconds.
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
- **Language**: The `Text Overlay` and `Voiceover` columns must be in colloquial Bahasa Malaysia.
- **Timestamp**: Indicate the start and end time for each segment (e.g., 0:00-0:03).
- **Visual**: Describe the visual elements of the scene.
- **Text Overlay**: Write any text that should appear on the screen (in Bahasa Malaysia).
- **Voiceover**: Write the spoken words for the script (in colloquial Bahasa Malaysia).

# Example

| Timestamp | Visual | Text Overlay | Voiceover |
| --- | --- | --- | --- |
| 0:00-0:03 | [Muka speaker nampak teruja] | Korang tahu tak? | "Eh, korang tahu tak perang paling sekejap dalam sejarah dunia cuma 38 minit je?" |
| 0:04-0:08 | [Gambar-gambar lama Perang Inggeris-Zanzibar] | 27 Ogos 1896 | "Betul weh! Perang Inggeris-Zanzibar tahun 1896. Zanzibar surrender lepas kena bedil dengan kapal British 38 minit je." |
| 0:09-0:15 | [Speaker kembali senyum kat skrin] | #sejarah #faktamenarik | "Nak tahu lagi fakta sejarah gila-gila macam ni? Follow aku!" |

# Notes
- Ensure the script suits a maximum of 60 seconds in length.
- Be mindful of creating an engaging narrative flow.
- Consider using trendy TikTok sound effects or edits where appropriate.
"""

def generate_script(topic, video_length):
    """Generates the TikTok script using the configured AI provider."""
    if not st.session_state.get("api_key"):
        st.error("Please enter your API key in the Settings tab.")
        return None
    if not st.session_state.get("model"):
        st.error("Please configure the model in the Settings tab.")
        return None

    try:
        provider = st.session_state.api_provider
        api_key = st.session_state.api_key
        model_name = st.session_state.model
        
        user_prompt = f"Create a {video_length}-second TikTok script about {topic}."

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
            return response.choices[0].message.content
        
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
            return response.choices[0].message.content

        elif provider == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            full_prompt = f"{SYSTEM_PROMPT}\n\n---\n\n{user_prompt}"
            response = model.generate_content(full_prompt)
            return response.text

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# --- UI Setup ---
tab_generator, tab_settings = st.tabs(["Script Generator", "Settings"])

with tab_generator:
    st.title("TikTok Script Generator")
    topic = st.text_input("Enter the topic for your TikTok video:")
    video_length = st.selectbox("Select video length (in seconds):", [15, 30, 60])

    if st.button("Generate Script"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating your script..."):
                script = generate_script(topic, video_length)
                if script:
                    st.subheader("Your TikTok Script:")
                    st.markdown(script)

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