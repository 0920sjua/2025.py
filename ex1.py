pip install streamlit torch torchvision pillow opencv-python
import io
import numpy as np
import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as T
from torchvision import models
import cv2

st.set_page_config(page_title="동물 분류 & 얼굴 탐지", page_icon="🐾", layout="wide")
st.title("🐾 동물 분류 & 🙂 얼굴 탐지 (신원 식별 없음)")

# -----------------------------
# 캐시된 모델 로더
# -----------------------------
@st.cache_resource
def load_imagenet_model():
    weights = models.ResNet50_Weights.DEFAULT  # ImageNet1K
    model = models.resnet50(weights=weights)
    model.eval()
    preprocess = weights.transforms()
    categories = weights.meta["categories"]
    return model, preprocess, categories

# -----------------------------
# 유틸: PIL 이미지 → torch 텐서 전처리
# -----------------------------
def prepare_image(pil_img, preprocess):
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")
    return preprocess(pil_img).unsqueeze(0)

# -----------------------------
# 예측 함수 (Top-k)
# -----------------------------
@torch.inference_mode()
def predict_topk(pil_img, model, preprocess, categories, k=5):
    inp = prepare_image(pil_img, preprocess)
    logits = model(inp)
    probs = torch.softmax(logits, dim=1)[0]
    topk = torch.topk(probs, k)
    results = []
    for score, idx in zip(topk.values.tolist(), topk.indices.tolist()):
        results.append((categories[idx], float(score)))
    return results

# -----------------------------
# 탭 구성
# -----------------------------
tab1, tab2 = st.tabs(["🦁 동물 분류", "🙂 얼굴 탐지(신원 식별 없음)"])

# -----------------------------
# 탭1: 동물 분류
# -----------------------------
with tab1:
    st.subheader("이미지 속 동물(또는 가장 가까운 클래스) 예측")
    st.caption("ImageNet 사전학습 모델(ResNet50)을 사용합니다. 동물 외 사물로 예측될 수도 있어요.")
    up1 = st.file_uploader("이미지를 업로드하세요 (jpg/png)", type=["jpg", "jpeg", "png"], key="animal")
    if up1 is not None:
        try:
            img = Image.open(io.BytesIO(up1.read()))
            st.image(img, caption="업로드한 이미지", use_column_width=True)
            with st.spinner("분석 중..."):
                model, preprocess, categories = load_imagenet_model()
                preds = predict_topk(img, model, preprocess, categories, k=5)

            st.success("예측 결과 (Top-5)")
            for i, (label, score) in enumerate(preds, start=1):
                st.write(f"{i}. **{label}** — {score*100:.2f}%")
        except Exception as e:
            st.error(f"처리 중 오류가 발생했어요: {e}")

# -----------------------------
# 탭2: 얼굴 탐지 (신원 식별 없음)
# -----------------------------
with tab2:
    st.subheader("얼굴 유무/개수 탐지 (신원 식별은 하지 않아요)")
    st.caption("OpenCV Haar Cascade로 얼굴을 감지하고 박스를 그려줍니다.")
    up2 = st.file_uploader("얼굴이 있는 이미지를 업로드하세요 (jpg/png)", type=["jpg", "jpeg", "png"], key="face")
    if up2 is not None:
        try:
            img = Image.open(io.BytesIO(up2.read()))
            if img.mode != "RGB":
                img = img.convert("RGB")

            # PIL → OpenCV BGR
            img_np = np.array(img)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # Haar Cascade 로드
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            face_cascade = cv2.CascadeClassifier(cascade_path)

            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

            # 박스 그리기
            for (x, y, w, h) in faces:
                cv2.rectangle(img_bgr, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # 다시 RGB로 변환 후 표시
            out_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            st.image(out_rgb, caption=f"감지된 얼굴 수: {len(faces)}", use_column_width=True)

            if len(faces) == 0:
                st.info("얼굴이 감지되지 않았어요. 다른 이미지를 시도해보세요.")
        except Exception as e:
            st.error(f"처리 중 오류가 발생했어요: {e}")

st.markdown("---")
st.caption(
    "안내: 이 앱은 사진 속 인물을 누구인지 **식별하지 않습니다**. "
    "동물 분류는 ImageNet 기반으로 추정 결과를 제공하며, 사진·각도·해상도에 따라 정확도가 달라질 수 있습니다."
)
streamlit run app.py

