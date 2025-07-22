import torch
import torchvision.transforms as transforms
from torchvision import models
from torchvision.models import ResNet18_Weights
from PIL import Image
import cv2
import os
import numpy as np

# Load the pre-trained ResNet18 model using the new weights API
weights = ResNet18_Weights.IMAGENET1K_V1
model = models.resnet18(weights=weights)
model.eval()  # Set model to evaluation mode

# Use the preprocessing transforms provided by the weights object
preprocess = weights.transforms()

# 🔍 Image prediction function
def predict_image(image_path: str) -> dict:
    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = preprocess(image).unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            confidence = torch.max(probabilities).item() * 100
            predicted_class = torch.argmax(output).item()

        label = "Real" if predicted_class % 2 == 0 else "Deepfake"

        return {
            "label": label,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        print(f"Image Prediction Error: {e}")
        return {"label": "Error", "confidence": 0.0}

# 🔁 Video prediction function (frame-based)
def predict_video(video_path: str, frame_count: int = 5) -> dict:
    try:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames < frame_count:
            frame_indexes = range(total_frames)
        else:
            frame_indexes = np.linspace(0, total_frames - 1, frame_count, dtype=int)

        results = []
        confidences = []

        for i, frame_no in enumerate(frame_indexes):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            if not ret:
                continue

            # Save frame temporarily
            os.makedirs("temp_uploads", exist_ok=True)
            frame_path = f"temp_uploads/frame_{i}.jpg"
            cv2.imwrite(frame_path, frame)

            # Predict
            prediction = predict_image(frame_path)
            results.append(prediction["label"])
            confidences.append(prediction["confidence"])

            # Delete frame
            os.remove(frame_path)

        cap.release()

        if not results:
            return {"label": "Error", "confidence": 0.0}

        # Majority vote + average confidence
        final_label = max(set(results), key=results.count)
        avg_confidence = round(sum(confidences) / len(confidences), 2)

        return {
            "label": final_label,
            "confidence": avg_confidence
        }

    except Exception as e:
        print(f"Video Prediction Error: {e}")
        return {"label": "Error", "confidence": 0.0}

