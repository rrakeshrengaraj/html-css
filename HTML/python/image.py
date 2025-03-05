import gradio as gr
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

# Load the model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Set generation parameters
max_length = 16
num_beams = 4

gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# Caption generation function
def generate_caption(image):
    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)
    
    output_ids = model.generate(pixel_values, **gen_kwargs)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    
    return preds[0]

# Create the chatbot interface
interface = gr.Interface(
    fn=generate_caption,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Image Captioning Chatbot",
    description="Upload an image, and the model will generate a caption for you!",
)

# Launch the chatbot
interface.launch()

# Run this script, and it will open a web page where you can upload an image and get a caption. Let me know if you’d like me to customize anything! 🚀
