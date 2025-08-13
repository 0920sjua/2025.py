# ---------- 라이브러리 자동 설치 ----------
import subprocess
import sys

packages = ["streamlit", "torch", "torchvision", "pillow", "opencv-python"]
for pkg in packages:
    try:
        __import__(pkg if pkg != "opencv-python" else "cv2")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# ---------- 실제 앱 코드 ----------
import io
import numpy as np
import streamlit as st
from PIL import Image
import torch
from torchvision import models

st.set_page_config(page_title="AI 동물 사전", page_icon="🦁", layout="wide")
st.title("🦁 AI 동물 사전")

# -----------------------------
# 동물 설명 데이터 (간단 예시)
# -----------------------------
animal_info = {
    "tiger": "호랑이: 고양잇과의 대형 맹수로, 아시아 전역에 서식하며 줄무늬가 특징입니다.",
    "lion": "사자: 아프리카와 인도 일부에 서식하는 대형 고양잇과 동물로, 수컷은 갈기가 있습니다.",
    "elephant": "코끼리: 지상에서 가장 큰 육상 동물로, 긴 코(코끼리 코)와 큰 귀가 특징입니다.",
    "zebra": "얼룩말: 흑백 줄무늬가 특징인 초식동물로, 주로 아프리카 초원에 서식합니다.",
    "dog": "개: 인류와 오랜 세월 함께 살아온 반려동물로, 다양한 품종이 존재합니다.",
    "cat": "고양이: 유연한 몸과 예리한 발톱을 가진 반려동물로, 독립적인 성격이 특징입니다.",
    "panda": "판다: 중국의 대나무 숲에 사는 대형 곰과 동물로, 흰 털과 검은 반점이 특징입니다.",
}

# -----------------------------
# 모델 로더
# -----------------------------
@st.cache_resource
def load_model():
    weights = models.ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)
    model.eval()
    preprocess = weights.transforms()
    categories = weights.meta["categories"]
    return model, preprocess, categories

# -----------------------------
# 이미지 전처리
# -----------------------------
def prepare_image(pil_img, preprocess):
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")
    return preprocess(pil_img).unsqueeze(0)

# -----------------------------
# 예측 함수
# -----------------------------
@torch.inference_mode()
def predict(pil_img, model, preprocess, categories):
    inp = prepare_image(pil_img, preprocess)
    logits = model(inp)
    probs = torch.softmax(logits, dim=1)[0]
    top_prob, top_idx = torch.max(probs, dim=0)
    return categories[top_idx], float(top_prob)

# -----------------------------
# UI
# -----------------------------
uploaded_file = st.file_uploader("동물 사진을 업로드하세요", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(io.BytesIO(uploaded_file.read()))
    st.image(img, caption="업로드한 이미지", use_column_width=True)

    with st.spinner("AI가 동물을 분석 중입니다..."):
        model, preprocess, categories = load_model()
        label, prob = predict(img, model, preprocess, categories)

    st.success(f"예측: **{label}** ({prob*100:.2f}%)")

    # 동물 정보 표시
    if label.lower() in animal_info:
        st.subheader("📚 동물 정보")
        st.write(animal_info[label.lower()])
    else:
        st.info("이 동물에 대한 사전 정보가 없습니다. (모델이 동물이 아닌 사물로 인식했을 수도 있어요)")
