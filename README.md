# Vendor Risk Summary Assistant

An AI-powered Streamlit app that helps Third-Party Risk Management (TPRM) analysts evaluate vendor risk and produce structured risk summaries.

---

## 1. Context, User, and Problem

**Who is the user?**
The user is a Third-Party Risk Management (TPRM) analyst or operational risk professional responsible for evaluating vendor risk within an organization such as a bank, insurance company, or healthcare organization.

**What workflow is being improved?**
The analyst receives vendor due diligence information — descriptions of services provided, data handled, certifications held, and access levels — and must produce a structured risk summary that includes a risk rating (High, Medium, or Low), key risks, and recommended controls.

**Why does this problem matter?**
This task is time-consuming, subjective, and inconsistent when done manually. Different analysts may rate the same vendor differently depending on experience and interpretation. Organizations that rely on third-party vendors must meet regulatory and internal risk management standards, making consistency and accuracy critical. GenAI is well suited here because it can interpret unstructured vendor descriptions, apply a structured rubric consistently, and generate formatted outputs that support analyst decision-making.

---

## 2. Solution and Design

**What was built?**
Two Streamlit apps:
- `app.py` — the main app using a structured system prompt with an explicit risk rubric
- `baseline_app.py` — a baseline app using a minimal unstructured prompt for comparison

**How it works:**
1. The analyst pastes vendor due diligence information into a text area
2. Clicks Analyze Risk
3. The app sends the input to Google Gemini with a system prompt
4. The model returns a structured risk summary displayed in the browser

**Key design choices:**

*Structured system prompt with explicit rubric:* The system prompt defines exactly what makes a vendor High, Medium, or Low risk. This directly addresses the challenge of getting a language model to apply rules consistently. High risk is triggered by sensitive or regulated data (PII, financial, health, HR/payroll), missing certifications, privileged system access, or offshore storage. Medium risk covers partial controls or limited exposure. Low risk requires no sensitive data, strong certifications, and limited access.

*Strict output format:* The prompt requires the model to always respond with the same four sections — Risk Rating, Key Risks, Recommended Controls, and Rationale — followed by an advisory disclaimer. This makes outputs easy to scan and compare.

*Incomplete information handling:* The prompt instructs the model to flag missing information explicitly rather than guess, and to assign a provisional rating pending further due diligence.

*No RAG, no agents, no fine-tuning:* The task is well-served by prompt engineering alone. Adding retrieval or multi-step orchestration would add complexity without improving the core workflow.

---

## 3. Evaluation and Results

**Baseline:**
The baseline app uses the prompt: *"You are a risk analyst. Review the vendor information provided and summarize the vendor's risk."* No rubric, no format requirements, no disclaimer instruction.

**Test set:**
12 synthetic vendor scenarios covering:
- Clear high risk (payroll processor, no SOC2, offshore storage)
- Clear low risk (digital signage, no sensitive data, SOC2 Type II)
- Medium risk (email marketing, PII, SOC2 Type I only)
- IT vendor with privileged access and offshore operations
- Strong certifications (SOC1, SOC2, ISO 27001)
- Incomplete information (one sentence, vague description)
- Regulated data (healthcare PHI, fintech PCI-DSS)
- Contradictory information (claims strong controls, no certifications)
- Multiple red flags simultaneously
- Low risk internal tool

**Evaluation rubric (1–3 scale per dimension):**
- Rating Accuracy — does the rating match the expected level given the scenario?
- Risk Completeness — are the key risks identified without obvious omissions?
- Control Relevance — are the recommended controls specific and appropriate?
- Output Consistency — is the format correct and disclaimer present?

**Results:**

| Finding | Structured Prompt | Baseline |
|---|---|---|
| Format consistent across all 12 scenarios | Yes | No |
| Advisory disclaimer included | 12/12 | 0/12 |
| Rating disagreements vs expected | 0/12 | 4/12 |
| Incomplete info handled explicitly | Yes | No |

**Rating disagreements (4 scenarios):**
Scenarios 3, 5, 7, and 8 produced different ratings between the two apps. In all four cases the structured prompt was more conservative — rating vendors as High when they handled regulated data (PII, PHI, financial) even when certifications were present. The baseline tended to downgrade ratings when certifications were strong, producing ratings like "Moderate-Low" or "Low to Moderate" that are not grounded in a consistent rubric.

**Edge cases:**
Scenarios 6 and 11 (incomplete vendor descriptions) showed the clearest difference. The structured prompt flagged each missing information item explicitly and assigned a provisional High rating with a clear rationale. The baseline produced long unfocused narratives without a clear conclusion.

**Where the project broke down:**
The rubric rates all vendors handling financial or health data as High regardless of certifications. A human analyst would likely treat strong certifications (PCI-DSS, HIPAA, SOC2 Type II) as meaningful mitigating factors that could lower the rating to Medium. This is a known limitation of strict rubric application and is intentional for a first-pass triage tool — the disclaimer always instructs human review before any decision is made.

---

## 4. Artifact Snapshot

**Main app — High Risk output:**

The app produces a color-coded risk badge (red for High, yellow for Medium, green for Low) followed by structured sections:

```
RISK RATING: HIGH

KEY RISKS:
- Handles highly sensitive employee PII (SSNs, bank account information)
- Lacks SOC2 certification for data processing
- Privileged access to internal HR systems
- Data stored on servers located outside the US

RECOMMENDED CONTROLS:
- Mandate SOC2 Type II report within a defined timeframe
- Implement strict access governance with MFA and least privilege
- Establish a Data Processing Addendum with breach notification requirements
- Review offshore data storage locations and associated regulations

RATIONALE:
CloudPay Inc. is assigned HIGH RISK due to multiple simultaneous high-risk factors...

⚠️ This output is advisory only and must be reviewed by a qualified risk analyst.
```

**Baseline output for the same input:**
The baseline produced a correct High rating but in an unstructured narrative format with no disclaimer, no controls section, and a different structure every time.

---

## Setup and Usage

**Requirements:**
- Python 3.10 or higher recommended
- A Google Gemini API key (from aistudio.google.com)

**Installation:**

```bash
git clone https://github.com/YOURUSERNAME/vendor-risk-assistant.git
cd vendor-risk-assistant
pip3 install -r requirements.txt
```

**Configuration:**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit this file. It is listed in `.gitignore`.

**Run the main app:**
```bash
python3 -m streamlit run app.py
```

**Run the baseline app (for comparison):**
```bash
python3 -m streamlit run baseline_app.py --server.port 8502
```

The app will open automatically in your browser at `http://localhost:8501`.

Paste vendor due diligence information into the text area and click **Analyze Risk** to generate a structured risk summary.

---

## Files

| File | Description |
|---|---|
| `app.py` | Main Streamlit app with structured prompt and rubric |
| `baseline_app.py` | Baseline app with unstructured prompt for comparison |
| `requirements.txt` | Python dependencies |
| `.env.example` | API key template |
| `.gitignore` | Prevents `.env` from being committed |

---

## Disclaimer

All outputs from this application are advisory only. Results must be reviewed by a qualified risk analyst before use in any risk decision or regulatory determination. This tool is intended to support analyst judgment, not replace it.
