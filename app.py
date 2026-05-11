import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a Third-Party Risk Management (TPRM) analyst assistant. Your job is to evaluate vendor information and produce a structured risk summary for use by a human risk analyst.

## Risk Rating Rubric

Use the following rubric to assign a risk rating. Apply it strictly and consistently.

**HIGH RISK** — One or more of the following:
- Handles sensitive or regulated data (PII, financial data, health/medical data, HR/payroll data)
- No security certifications (SOC1, SOC2, ISO 27001, HIPAA, PCI-DSS) or certifications are expired
- Has privileged or administrative access to internal systems
- Stores or processes data offshore in high-risk jurisdictions
- Provides critical or hard-to-replace services with no redundancy
- Multiple red flags present simultaneously

**MEDIUM RISK** — One or more of the following, without High Risk factors:
- Limited access to sensitive data but some exposure exists
- Some security controls in place but notable gaps identified
- Certifications present but incomplete for the data handled
- Moderate dependency with available alternatives

**LOW RISK** — All of the following:
- No access to sensitive or regulated data
- Strong, relevant certifications in place (e.g., SOC2 Type II)
- Well-defined and limited access controls
- Non-critical service with easily available alternatives

## Instructions

1. Read the vendor information carefully.
2. Identify the key risks based on the rubric above.
3. Assign a risk rating of HIGH, MEDIUM, or LOW.
4. Recommend specific controls appropriate to the risks identified.
5. If the vendor description is incomplete or ambiguous, flag the missing information explicitly and note that the rating may need revision once complete information is available. Do not guess.
6. Never make a definitive risk decision — your output is advisory only.

## Required Output Format

Always respond in exactly this format:

**RISK RATING:** [HIGH / MEDIUM / LOW]

**KEY RISKS:**
- [Risk 1]
- [Risk 2]
- [Risk 3]

**RECOMMENDED CONTROLS:**
- [Control 1]
- [Control 2]
- [Control 3]

**RATIONALE:**
[One paragraph explaining the rating, connecting the vendor's specific characteristics to the rubric criteria.]

---
⚠️ *This output is advisory only and must be reviewed by a qualified risk analyst before use in any risk decision or regulatory determination.*
"""

def analyze_vendor(vendor_info: str) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    response = model.generate_content(vendor_info)
    return response.text


def main():
    st.set_page_config(
        page_title="Vendor Risk Summary Assistant",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Vendor Risk Summary Assistant")
    st.caption("AI-powered risk summarization for Third-Party Risk Management analysts")

    st.info(
        "Paste vendor due diligence information below and click Analyze Risk. "
        "The assistant will return a structured risk summary including a risk rating, "
        "key risks, and recommended controls.",
        icon="ℹ️"
    )

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Vendor Information")
        vendor_input = st.text_area(
            label="Paste vendor information here",
            placeholder=(
                "Example: CloudPay Inc. provides payroll processing services and handles "
                "sensitive employee PII including SSNs and bank account information. "
                "The vendor does not hold a SOC2 certification and stores data on servers "
                "located outside the US..."
            ),
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
                    result = analyze_vendor(vendor_input)

                    if "RISK RATING:** HIGH" in result:
                        st.error("HIGH RISK", icon="🔴")
                    elif "RISK RATING:** MEDIUM" in result:
                        st.warning("MEDIUM RISK", icon="🟡")
                    elif "RISK RATING:** LOW" in result:
                        st.success("LOW RISK", icon="🟢")

                    st.markdown(result)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.markdown(
                "<div style='color: #888; padding: 2rem 0;'>Results will appear here after you submit vendor information.</div>",
                unsafe_allow_html=True
            )

    st.divider()
    st.caption(
        "⚠️ All outputs are advisory only. Results must be reviewed by a qualified risk analyst "
        "before use in any risk decision or regulatory determination."
    )


if __name__ == "__main__":
    main()