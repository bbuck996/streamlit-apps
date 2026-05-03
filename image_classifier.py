import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import streamlit as st
import torch
from torchvision import transforms, models
from torchvision.models import ResNet50_Weights
from PIL import Image

# Page title and instructions
st.title('🖼️ Image Classifier')
st.write('Upload an image and I will tell you what it is using a pretrained AI model!')
st.write('**Instructions:** Click the button below to upload a JPG or PNG image.')

# Load pretrained model
@st.cache_resource
def load_model():
    weights = ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)
    model.eval()
    return model, weights

model, weights = load_model()

LABELS = weights.meta["categories"]

# Image upload
uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_column_width=True)

    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    input_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5_prob, top5_idx = torch.topk(probabilities, 5)

    st.header('🔍 Predictions')
    for i in range(5):
        label = LABELS[top5_idx[i].item()]
        prob = top5_prob[i].item() * 100
        st.write(f'**{i+1}. {label}** — {prob:.2f}%')
        st.progress(top5_prob[i].item())