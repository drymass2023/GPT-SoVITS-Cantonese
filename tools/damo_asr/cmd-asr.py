import os
import sys
import traceback
from transformers import pipeline
import torch

# Assuming the first argument is the script name and the second one is the directory
dir = sys.argv[1]
opt_name = os.path.basename(dir)

MODEL_NAME = "jed351/whisper_medium_cantonese_cm_voice"
lang = "zh"

# Check for CUDA availability for GPU support
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialize the pipeline with the specified model
pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    device=device,
)

opt = []  # List to hold the output strings
opt_dir = "output/asr_opt"
os.makedirs(opt_dir, exist_ok=True)  # Ensure the directory for the results file exists

# Process each file in the input directory
for name in os.listdir(dir):
    try:
        # Ensure we are only processing audio files, typically '.mp3' or '.wav'
        if name.endswith('.mp3') or name.endswith('.wav'):
            file_path = os.path.join(dir, name)
            # Call your pipeline to obtain the transcription
            text = pipe(file_path)["text"]
            opt.append(f"{dir}/{name}|{opt_name}|ZH|{text}")
        else:
            continue
    except Exception as e:
        # Handle exceptions and display the traceback
        print(f"An error occurred while processing {name}:")
        print(traceback.format_exc())

# Write all transcriptions to a file in the opt_dir
with open(f"{opt_dir}/{opt_name}.list", "w", encoding="utf-8") as f:
    f.write("\n".join(opt))

print(f"All transcriptions have been saved to {opt_dir}/{opt_name}.list")
