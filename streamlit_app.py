import streamlit as st
import cv2
import numpy as np
import joblib
from deepface import DeepFace
import qrcode
import io
import base64
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="顔から分かる動物タイプ診断",
    page_icon="🐾",
    layout="centered"
)

# CSS 스타일 적용
st.markdown("""
    <style>
        .main {
            max-width: 600px;
            margin: 0 auto;
        }
        .title {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .result-box {
            background-color: #fef3c7;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
        }
        .animal-name {
            color: #e17055;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 모델 및 레이블 인코더 로드 (캐시)
@st.cache_resource
def load_models():
    model = joblib.load('models/animal_onlyface100_model.pkl')
    le = joblib.load('models/label_onlyface100_encoder.pkl')
    return model, le

# 클래스 리스트
classes = ['다람쥐', '고양이', '사슴', '공룡', '강아지', '여우', '말', '토끼', '거북이', '늑대']

# 클래스 이름 일본어 변환
animal_name_ja = {
    '다람쥐': 'リス',
    '고양이': '猫',
    '사슴': '鹿',
    '공룡': '恐竜',
    '강아지': '犬',
    '여우': '狐',
    '말': '馬',
    '토끼': '兎',
    '거북이': '亀',
    '늑대': '狼'
}

# 얼굴 인식 함수
def detect_face(image_array):
    """이미지에서 얼굴 감지"""
    try:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face = image_array[y:y + h, x:x + w]
            return face, (x, y, w, h)
        else:
            return None, None
    except Exception as e:
        st.error(f"얼굴 인식 중 오류 발생: {e}")
        return None, None

# 이미지 분류 함수
def classify_image(face_image):
    """얼굴 이미지 분류"""
    try:
        model, le = load_models()
        
        # PIL 이미지를 numpy 배열로 변환하여 임시 저장
        face_pil = Image.fromarray(face_image)
        temp_path = "temp_face.jpg"
        face_pil.save(temp_path)
        
        # DeepFace 임베딩 추출
        embedding = DeepFace.represent(
            temp_path,
            model_name="VGG-Face",
            enforce_detection=False
        )[0]["embedding"]
        
        embedding = np.array(embedding).reshape(1, -1)
        probabilities = model.predict_proba(embedding)[0]
        
        results = []
        for idx, prob in enumerate(probabilities):
            animal_class_kr = classes[idx]
            animal_class_ja = animal_name_ja.get(animal_class_kr, animal_class_kr)
            animal_probability = prob * 100
            
            results.append({
                "animal": animal_class_ja,
                "probability": animal_probability
            })
        
        return sorted(results, key=lambda x: x["probability"], reverse=True)
    except Exception as e:
        st.error(f"분류 중 오류 발생: {e}")
        return None

# QR 코드 생성 함수
def generate_qr_code():
    """앱 URL의 QR 코드 생성"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("https://faceai-animal.streamlit.app")
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        return qr_image
    except Exception as e:
        st.error(f"QR 코드 생성 중 오류: {e}")
        return None

# 제목
st.markdown("<div class='title'>🐾 顔から分かる動物タイプ診断 🐾</div>", unsafe_allow_html=True)
st.write("あなたの顔から、どの動物タイプか診断します！")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📸 診断", "ℹ️ 使い方", "🔗 QRコード"])

with tab1:
    st.subheader("写真をアップロード")
    
    # 파일 업로더
    uploaded_file = st.file_uploader("画像ファイルを選択してください", type=['jpg', 'jpeg', 'png', 'bmp'])
    
    if uploaded_file is not None:
        # 이미지 로드
        image = Image.open(uploaded_file)
        image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**アップロード画像**")
            st.image(image, use_column_width=True)
        
        with col2:
            st.write("**検出された顔**")
            
            # 얼굴 감지
            face_image, coords = detect_face(image_array)
            
            if face_image is not None:
                face_display = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                face_pil = Image.fromarray(face_display)
                st.image(face_pil, use_column_width=True)
            else:
                st.warning("顔が検出されませんでした")
        
        # 분류 버튼
        if st.button("🔍 診断結果を表示", use_container_width=True):
            if face_image is not None:
                with st.spinner("診断中..."):
                    results = classify_image(face_image)
                    
                    if results:
                        # 최상위 결과
                        top_result = results[0]
                        st.markdown(f"""
                        <div class='result-box'>
                            <div>あなたの動物タイプは...</div>
                            <div class='animal-name'>{top_result['animal']}</div>
                            <div style='margin-top: 10px; font-size: 16px;'>
                                一致度: {top_result['probability']:.1f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 모든 결과 표시
                        st.subheader("📊 全ての診断結果")
                        result_data = []
                        for r in results:
                            result_data.append({
                                "動物": r['animal'],
                                "一致度 (%)": f"{r['probability']:.2f}%"
                            })
                        
                        st.dataframe(result_data, use_container_width=True, hide_index=True)
                    else:
                        st.error("診断に失敗しました")
            else:
                st.error("顔を検出できませんでした。別の画像をお試しください。")

with tab2:
    st.subheader("使い方")
    st.write("""
    1. 📸 写真をアップロードしてください
    2. 明るい場所で、正面を向いた顔写真がおすすめです
    3. 🔍 診断結果を表示ボタンをクリック
    4. あなたの動物タイプが表示されます！
    
    **対応する動物タイプ:**
    """)
    
    animals_display = []
    for kr, ja in animal_name_ja.items():
        animals_display.append(f"• {ja}")
    
    st.write("\n".join(animals_display))

with tab3:
    st.subheader("このアプリを共有")
    qr_img = generate_qr_code()
    if qr_img:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(qr_img, caption="QRコード", use_column_width=True)
        with col2:
            st.write("**アプリのリンク:**")
            st.code("https://faceai-animal.streamlit.app")
    
    st.info("このQRコードをスキャンするか、リンクをシェアしてください！")
