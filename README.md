#  Meeting Minutes via Voice

Industrial-Ready MP3 → Transcript → Structured Board Minutes (Fully
Local)

------------------------------------------------------------------------

##  What This System Does

-   Converts MP3 (auto 16kHz mono) → text using Whisper
-   Transforms transcript → board-grade structured minutes
-   Enforces 9 mandatory Markdown sections
-   Saves `meeting_minutes.md` automatically
-   Auto-detects GPU (≈2--4× faster with CUDA)

------------------------------------------------------------------------

##  Live Deployed Version

Hugging Face Space (Deployed App):
https://huggingface.co/spaces/Pd18/Meeting_Minutes

------------------------------------------------------------------------

#  4-Step Processing Pipeline

1.  Load & Resample Audio (16kHz mono)
2.  Transcribe in 45s chunks (2s overlap reduces word loss)
3.  Generate structured minutes (temperature = 0 → deterministic
    output)
4.  Render + Save Markdown

------------------------------------------------------------------------

#  Core Configuration

-   whisper_model_name = "openai/whisper-base.en"
-   minutes_model_name = "gpt-oss:120b-cloud"
-   max_transcript_characters = 14000 for V1 but NONE in V2
-   chunk_length_seconds = 45

### Engineering Rationale

-   45s Chunking → Handles long recordings reliably
-   14,000 Character Cap in V1 → Prevents LLM overload
-   Temperature 0 → Ensures repeatable outputs
-   Timestamp Injection → Improves Traceability

------------------------------------------------------------------------

#  Output Guarantees

The model strictly produces:

1.  Meeting Summary (6--8 sentences)
2.  Attendees
3.  Agenda
4.  Key Discussion Points (2--4 bullets per topic + timestamps)
5.  Decisions Made
6.  Action Items
7.  Votes / Motions
8.  Risks / Blockers
9.  Next Steps

 No Transcript Copying 
 No Hallucinated Decisions
 Explicit-only Action Extraction
 Clean Professional Markdown

------------------------------------------------------------------------

#  Built-In Reliability Features

-   Auto GPU/CPU Detection (float16 vs float32)
-   Duplicate Transcript Filtering
-   Silent Token Streaming (clean console)
-   Deterministic LLM Generation
-   Character-Length Safety Control

------------------------------------------------------------------------

#  Industrial Usability

Suitable for:

Corporate & Board Governance
- Board Meetings
- Investor Reviews
- Compliance Documentation
- Audit-Ready Records

Public Sector & Councils
- Municipal Meetings
- Committee Sessions
- Policy Discussions

Enterprise Operations
- Strategy Reviews
- Cross-Functional Meetings
- Risk Assessment Sessions

------------------------------------------------------------------------

#  Required Packages

pip install torch torchvision torchaudio
pip install librosa transformers openai ipython
pip install sentencepiece accelerate notebook

------------------------------------------------------------------------

#  Ollama Setup

ollama pull gpt-oss:120b-cloud
ollama serve

------------------------------------------------------------------------

#  Run Instructions

python -m venv venv
source venv/Scripts/activate
jupyter notebook

Execute all cells → Output:

-   meeting_minutes.md\
-   Structured Board-Ready Minutes

------------------------------------------------------------------------

#  Final Outcome

This system:

-   Processes long meetings reliably
-   Produces structured governance-ready documentation
-   Reduces manual note-taking effort significantly
-   Maintains confidentiality (fully local execution)
-   Scales across enterprise workflows

# Note
- I have intenionally added multiple comments in each line of code because It was quiet complicated for me when I first started working on
it. Plus these comments will help me to revise the code work flow when I revisit it.
- V2.ipynb can create Meeting Minutes transcript for more than hour long meeting. While V1.ipynb can be used for shorter meeting around 30-45 min.
