import os

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

MODEL_PATH = 'ivan_laptop_2.pt'
IMG_SIZE = 96
DEVICE = torch.device('cpu')
SELECTED_CLASSES = [
    'Acne And Rosacea Photos',
    'Actinic Keratosis Basal Cell Carcinoma And Other Malignant Lesions',
    'Atopic Dermatitis Photos',
    'Bullous Disease Photos',
    'Eczema Photos',
    'Fu Athlete Foot',
    'Fu Nail Fungus',
    'Fu Ringworm',
    'Hair Loss Photos Alopecia And Other Hair Diseases',
    'Herpes Hpv And Other Stds Photos',
    'Melanoma Skin Cancer Nevi And Moles',
    'Urticaria Hives',
    'Heathy',
]


class LightSkinNet(nn.Module):
    def __init__(self, num_classes: int = 16) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.15),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.25),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.35),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Sequential(nn.Dropout(0.5), nn.Linear(256, num_classes))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


predict_tfms = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def load_model(model_path: str, num_classes: int = 16) -> LightSkinNet:
    model = LightSkinNet(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model


def predict_skin_disease(image_path: str) -> tuple:
    """
    Возвращает:
    (predicted_class_name: str, confidence_percent: float, class_idx: int)
    """
    model_path = 'ivan_laptop_2.pt'
    if not os.path.exists(image_path):
        return None, 0.0, None

    # Загружаем модель только один раз
    global _loaded_model
    if '_loaded_model' not in globals():
        _loaded_model = load_model(model_path, num_classes=len(SELECTED_CLASSES))

    image = Image.open(image_path).convert('RGB')
    input_tensor = predict_tfms(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = _loaded_model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)

    confidence, class_idx = torch.max(probabilities, dim=1)
    confidence = confidence.item() * 100

    class_idx = class_idx.item() + 1
    return class_idx, confidence
