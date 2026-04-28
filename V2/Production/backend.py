import torch
import gradio as gr # Required for gr.Progress type hint
from faster_whisper import WhisperModel
from openai import OpenAI
from jiwer import wer, cer

# ==========================================
# Configuration and Settings
# ==========================================

WHISPER_SIZE = "medium" 
AI_MODEL_NAME = "gpt-oss:120b-cloud"
TEXT_CHUNK_SIZE = 12000 
MAX_PROMPT_SIZE = 30000 

IS_GPU_AVAILABLE = torch.cuda.is_available()
COMPUTE_TYPE = "int8_float16" if IS_GPU_AVAILABLE else "float32"
DEVICE = "cuda" if IS_GPU_AVAILABLE else "cpu"

ai_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

CHUNK_SYSTEM_PROMPT = """You are a professional scribe. Extract ALL critical information.
Capture every decision, action item, and key argument. Maintain timestamps.
Output detailed notes for this section."""

FINAL_SYSTEM_PROMPT = """You are an expert corporate secretary. Consolidate these summaries into professional meeting minutes.

STRICT RULES:
1. Under '# Meeting Duration', write the exact duration provided.
2. Output ONLY Markdown.
3. Combine similar topics into cohesive discussion points.
4. Ensure NO action item or decision is lost.

Use EXACT headings:
# Meeting Summary
# Meeting Duration
# Attendees
# Agenda
# Key Discussion Points
# Decisions Made
# Action Items
# Votes / Motions
# Risks / Blockers
# Next Steps
""".strip()

# ==========================================
# Helper Functions
# ==========================================

def load_whisper_model():
    """Initializes the audio-to-text model."""
    return WhisperModel(WHISPER_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

whisper_model = load_whisper_model()

def format_time(seconds_value):
    """Converts seconds into a readable format."""
    seconds_value = int(seconds_value)
    minutes, seconds = divmod(seconds_value, 60)
    
    if minutes >= 60:
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    return f"{minutes:02d}:{seconds:02d}"

def get_audio_text(audio_file):
    """Transcribes audio file into text with timestamps."""
    segments, info = whisper_model.transcribe(audio_file, beam_size=5)
    
    text_with_time = [] 
    plain_text_list = [] 
    
    for segment in segments:
        timestamp = format_time(segment.start)
        text = segment.text.strip()
        
        if text:
            text_with_time.append(f"[{timestamp}] {text}")
            plain_text_list.append(text)
            
    total_duration = format_time(info.duration)
    return "\n".join(text_with_time), " ".join(plain_text_list), total_duration

def ask_ai_model(system_prompt, user_content):
    """Sends a request to the AI model and returns the text response."""
    response = ai_client.chat.completions.create(
        model=AI_MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0 
    )
    return response.choices[0].message.content

def check_text_quality(reference_text, ai_text):
    """Compares AI text to a reference text to check for errors."""
    if not reference_text or not ai_text:
        return "No reference text provided. Quality metrics skipped."
    
    ref_clean = reference_text.lower().strip()
    ai_clean = ai_text.lower().strip()
    
    word_error_rate = wer(ref_clean, ai_clean) * 100
    char_error_rate = cer(ref_clean, ai_clean) * 100
    
    if word_error_rate < 10:
        status = "⭐ Excellent"
    elif word_error_rate < 20:
        status = "👍 Good"
    else:
        status = "⚠️ Review required"
        
    return f"WER: {word_error_rate:.2f}%\nCER: {char_error_rate:.2f}%\n\nStatus: {status}"

# ==========================================
# Main Pipeline Logic
# ==========================================

def run_meeting_pipeline(audio_file, reference_text, progress=gr.Progress()):
    """Main workflow: Audio -> Transcript -> Quality Check -> AI Summary -> Minutes."""
    
    if audio_file is None:
        yield "❌ Please upload or record audio.", "", "", ""

    yield "🚀 Transcribing...", "", "", ""
    progress(0.2, desc="Transcribing Audio...")
    try:
        full_transcript, clean_transcript, total_duration = get_audio_text(audio_file)
    except Exception as e:
        yield f"❌ Transcription Error: {str(e)}", "", "", ""
        return

    yield "📊 Calculating quality metrics...", full_transcript, "", ""
    progress(0.4, desc="Evaluating...")
    metrics_result = check_text_quality(reference_text, clean_transcript)

    yield "✍️ Analyzing transcript in chunks...", full_transcript, metrics_result, ""
    
    transcript_chunks = [
        full_transcript[i : i + TEXT_CHUNK_SIZE] 
        for i in range(0, len(full_transcript), TEXT_CHUNK_SIZE)
    ]
    
    chunk_summaries = []
    for idx, chunk in enumerate(transcript_chunks):
        progress_val = 0.4 + (0.4 * (idx + 1) / len(transcript_chunks))
        progress(progress_val, desc=f"Processing chunk {idx+1}/{len(transcript_chunks)}...")
        
        summary = ask_ai_model(CHUNK_SYSTEM_PROMPT, f"Chunk {idx+1} of {len(transcript_chunks)}:\n{chunk}")
        chunk_summaries.append(summary)

    combined_summaries = "\n\n--- Section ---\n\n".join(chunk_summaries)
    
    if len(combined_summaries) > MAX_PROMPT_SIZE:
        yield "🌀 Condensing summaries for long meeting...", full_transcript, metrics_result, ""
        summary_chunks = [
            combined_summaries[i : i + MAX_PROMPT_SIZE] 
            for i in range(0, len(combined_summaries), MAX_PROMPT_SIZE)
        ]
        condensed_list = []
        for s_chunk in summary_chunks:
            condensed_list.append(ask_ai_model("Summarize this section while keeping key decisions.", s_chunk))
        combined_summaries = "\n\n".join(condensed_list)

    yield "🪄 Finalizing global meeting minutes...", full_transcript, metrics_result, ""
    
    final_user_input = f"--- MANDATORY DATA ---\nTOTAL MEETING DURATION: {total_duration}\n--- END DATA ---\n\nSUMMARIES:\n{combined_summaries}"
    
    try:
        final_response = ai_client.chat.completions.create(
            model=AI_MODEL_NAME,
            messages=[
                {"role": "system", "content": FINAL_SYSTEM_PROMPT},
                {"role": "user", "content": final_user_input},
            ],
            temperature=0,
            stream=False 
        )
        final_minutes = final_response.choices[0].message.content
    except Exception as e:
        yield f"❌ Final Synthesis Error: {str(e)}", full_transcript, metrics_result, ""
        return

    progress(1.0, desc="Done!")
    yield "✅ All Process Completed!", full_transcript, metrics_result, final_minutes
