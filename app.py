import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd

# -----------------------------------------------------------
# LANGUAGE LISTS
# -----------------------------------------------------------
lang_codes = ["en", "hi", "ta", "te", "ml", "fr", "es", "de", "ar", "zh-CN"]
lang_names = [
    "English",
    "Hindi",
    "Tamil",
    "Telugu",
    "Malayalam",
    "French",
    "Spanish",
    "German",
    "Arabic",
    "Chinese (Simplified)"
]
lang_map = dict(zip(lang_names, lang_codes))

# -----------------------------------------------------------
# SESSION STATE FOR HISTORY
# -----------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------
# TRANSLATION FUNCTION
# -----------------------------------------------------------
def translate_text(text, target_lang_code):
    try:
        return GoogleTranslator(source='auto', target=target_lang_code).translate(text)
    except Exception as e:
        return f"Error: {e}"

# -----------------------------------------------------------
# PAGE STYLE & BACKGROUND IMAGE
# -----------------------------------------------------------
st.set_page_config(page_title="Multi-language Translator", layout="wide")

# Use this background image — your URL
bg_image_url = "https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjEwMTYtYy0wOF8xLWtzaDZtemEzLmpwZw.jpg.jpg"

st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("{bg_image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------
# PAGE TITLE
# -----------------------------------------------------------
st.title("🌎 Multi-language Translator with Text & Documents")
st.write("Enter text, choose languages, translate, upload documents, and track translation history.")

# -----------------------------------------------------------
# MAIN LAYOUT
# -----------------------------------------------------------
left, right = st.columns(2)

# -----------------------------------------------------------
# LEFT SIDE — TEXT TRANSLATION
# -----------------------------------------------------------
with left:
    st.subheader("Translate Text")
    user_text = st.text_area("Enter text:", height=180)
    selected_langs = st.multiselect("Select target language(s):", lang_names)

    if st.button("Translate Text"):
        if user_text.strip() == "":
            st.warning("Please enter text.")
        elif len(selected_langs) == 0:
            st.warning("Please select at least one language.")
        else:
            for lang in selected_langs:
                code = lang_map[lang]
                translated = translate_text(user_text, code)
                st.success(f"**{lang}:** {translated}")
                st.session_state.history.append(
                    ("Text Input", user_text, lang, translated)
                )

# -----------------------------------------------------------
# RIGHT SIDE — DOCUMENT TRANSLATION
# -----------------------------------------------------------
with right:
    st.subheader("Upload Document")
    uploaded = st.file_uploader("Upload TXT or PDF", type=["txt", "pdf"])
    doc_target = st.selectbox("Select target language for file:", lang_names)

    if st.button("Translate Uploaded File"):
        if uploaded is None:
            st.warning("Please upload a file.")
        else:
            if uploaded.type == "text/plain":
                file_text = uploaded.read().decode("utf-8")
            elif uploaded.type == "application/pdf":
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded)
                file_text = ""
                for page in reader.pages:
                    file_text += page.extract_text()

            translated = translate_text(file_text, lang_map[doc_target])
            st.success("File Translated Successfully!")
            st.write(translated)
            st.session_state.history.append(
                ("Uploaded File", uploaded.name, doc_target, translated)
            )

# -----------------------------------------------------------
# HISTORY TABLE
# -----------------------------------------------------------
st.subheader("📜 Translation History")

if len(st.session_state.history) == 0:
    st.info("No translations yet.")
else:
    df = pd.DataFrame(
        st.session_state.history,
        columns=["Source Type", "Original Text", "Target Language", "Translated Text"]
    )
    st.dataframe(df, use_container_width=True)

if st.button("Clear History"):
    st.session_state.history = []
    st.success("History cleared!")
