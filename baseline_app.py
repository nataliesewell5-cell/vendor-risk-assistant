import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

BASELINE_SYSTEM_PROMPT = """
You are a risk analyst. Review the vendor information provided and summarize the vendor's risk.
"""

def analyze_vendor_baseline(vendor_info: str) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=BASELINE_SYSTEM_PROMPT
    )
    response = model.generate_content(vendor_info)
    return response.text


def main():
    st.set_page_config(
        page_title="Vendor Risk Assistant (Baseline)",
        page_icon="📋",
        layout="wide"
    )

    st.title("📋 Vendor Risk Assistant — Baseline")
    st.caption("Unstructured prompt baseline for evaluation comparison")

    st.warning(
        "This is the baseline version using an unstructured prompt, for evaluation comparison only.",
        icon="⚠️"
    )

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Vendor Information")
        vendor_input = st.text_area(
            label="Paste vendor information here",
            placeholder="Paste vendor due diligence information here...",
            height=350,
            label_visibility="collapsed"
        )

        analyze_button = st.button(
            "Analyze Risk",
            type="primary",
            use_container_width=True,
            disabled=not vendor_input.strip()
        )

    with col2:
        st.subheader("Risk Summary")

        if analyze_button and vendor_input.strip():
            with st.spinner("Analyzing vendor risk..."):
                try:
                    result = analyze_vendor_baseline(vendor_input)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.markdown(
                "<div style='color: #888; padding: 2rem 0;'>Results will appear here after you submit vendor information.</div>",
                unsafe_allow_html=True
            )

    st.divider()
    st.caption("Baseline app for academic evaluation purposes only.")


if __name__ == "__main__":
    main()