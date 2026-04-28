import gradio as gr
from backend import run_meeting_pipeline # Import logic from backend.py

# ==========================================
# Gradio UI Interface
# ==========================================

with gr.Blocks(title="AI Meeting Minutes Pro") as demo:
    gr.Markdown("# 📝 AI Meeting Minutes Professional")
    gr.Markdown("Optimized for very long meetings.")

    with gr.Tabs():
        with gr.Tab("1. Setup & Generate"):
            with gr.Row():
                with gr.Column():
                    # FIX: Added sources=["upload", "microphone"] to prevent glitching/vanishing
                    audio_input = gr.Audio(
                        label="Meeting Audio File", 
                        type="filepath", 
                        sources=["upload", "microphone"]
                    )
                    ref_input = gr.Textbox(label="Reference Transcript (Optional)", lines=5)
                    generate_btn = gr.Button("Start Processing", variant="primary")
                    status_box = gr.Textbox(label="Current Status", value="Ready", interactive=False)

        with gr.Tab("2. Full Transcript"):
            transcript_display = gr.Textbox(label="AI Generated Transcript", lines=20, interactive=False)
        with gr.Tab("3. Quality Metrics"):
            metrics_display = gr.Textbox(label="WER/CER Analysis", lines=5, interactive=False)
        with gr.Tab("4. Meeting Minutes"):
            minutes_display = gr.Markdown(label="Final Minutes")

    generate_btn.click(
        fn=run_meeting_pipeline,
        inputs=[audio_input, ref_input],
        outputs=[status_box, transcript_display, metrics_display, minutes_display]
    )

if __name__ == "__main__":
    demo.launch()
