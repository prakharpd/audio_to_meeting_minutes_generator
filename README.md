# 📄 Meeting Minutes via Voice

Industrial-Ready MP3 → Transcript → Structured Board Minutes (Fully
Local)

------------------------------------------------------------------------

## 🚀 What This System Does

-   Converts MP3 (auto 16kHz mono) → text using Whisper\
-   Transforms transcript → board-grade structured minutes\
-   Enforces 9 mandatory Markdown sections\
-   Saves `meeting_minutes.md` automatically\
-   Auto-detects GPU (≈2--4× faster with CUDA)

------------------------------------------------------------------------

## 🌐 Live Deployed Version

Hugging Face Space (Deployed App):\
https://huggingface.co/spaces/Pd18/Meeting_Minutes

------------------------------------------------------------------------

# 🔁 4-Step Processing Pipeline

1.  Load & Resample Audio (16kHz mono)\
2.  Transcribe in 45s chunks (2s overlap reduces word loss)\
3.  Generate structured minutes (temperature = 0 → deterministic
    output)\
4.  Render + Save Markdown

------------------------------------------------------------------------

# ⚙️ Core Configuration

-   whisper_model_name = "openai/whisper-base.en"
-   minutes_model_name = "gpt-oss:120b-cloud"
-   max_transcript_characters = 14000
-   chunk_length_seconds = 45

### Engineering Rationale

-   45s chunking → Handles long recordings reliably\
-   14,000 character cap → Prevents LLM overload\
-   Temperature 0 → Ensures repeatable outputs\
-   Timestamp injection → Improves traceability

------------------------------------------------------------------------

# 🎯 Output Guarantees

The model strictly produces:

1.  Meeting Summary (6--8 sentences)\
2.  Attendees\
3.  Agenda\
4.  Key Discussion Points (2--4 bullets per topic + timestamps)\
5.  Decisions Made\
6.  Action Items\
7.  Votes / Motions\
8.  Risks / Blockers\
9.  Next Steps

✔ No transcript copying\
✔ No hallucinated decisions\
✔ Explicit-only action extraction\
✔ Clean professional Markdown

------------------------------------------------------------------------

# 🧠 Built-In Reliability Features

-   Auto GPU/CPU detection (float16 vs float32)\
-   Duplicate transcript filtering\
-   Silent token streaming (clean console)\
-   Deterministic LLM generation\
-   Character-length safety control

------------------------------------------------------------------------

# 🏭 Industrial Usability

Suitable for:

Corporate & Board Governance\
- Board meetings\
- Investor reviews\
- Compliance documentation\
- Audit-ready records

Public Sector & Councils\
- Municipal council meetings\
- Committee sessions\
- Policy discussions

Enterprise Operations\
- Strategy reviews\
- Cross-functional meetings\
- Risk assessment sessions

------------------------------------------------------------------------

# 📦 Required Packages

pip install torch torchvision torchaudio\
pip install librosa transformers openai ipython\
pip install sentencepiece accelerate notebook

------------------------------------------------------------------------

# 🦙 Ollama Setup

ollama pull gpt-oss:120b-cloud\
ollama serve

------------------------------------------------------------------------

# ▶️ Run Instructions

python -m venv venv\
source venv/Scripts/activate\
jupyter notebook

Execute all cells → Output:

-   meeting_minutes.md\
-   Structured board-ready minutes

------------------------------------------------------------------------

# 🏁 Final Outcome

This system:

-   Processes long meetings reliably\
-   Produces structured governance-ready documentation\
-   Reduces manual note-taking effort significantly\
-   Maintains confidentiality (fully local execution)\
-   Scales across enterprise workflows
