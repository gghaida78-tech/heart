import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
import os

# تحميل النموذج (مسار نسبي)
model_path = os.path.join(os.path.dirname(__file__), "heart_model.pkl")
model = joblib.load(model_path)

# إعداد الصفحة
st.set_page_config(
    page_title="💓 نظام تنبؤ أمراض القلب",
    page_icon="❤️",
    layout="centered"
)

# خلفية بيضاء وتصغير حجم الحقول
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    .stSlider > div, .stSelectbox > div, .stRadio > div, .stTextInput > div {
        max-width: 400px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# تسجيل الدخول
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.header("🔐 تسجيل الدخول")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if password == "1234":
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.page = "form"
            st.toast(f"مرحباً {username}! تم تسجيل الدخول بنجاح 👋", icon="✅")
        else:
            st.error("كلمة المرور غير صحيحة.")
    st.stop()

# صفحة إدخال البيانات
if "page" not in st.session_state:
    st.session_state.page = "form"

if st.session_state.page == "form":
    st.header(f"🩺 مرحباً {st.session_state.username}, أدخل بياناتك الطبية")

    age = st.slider("👶 العمر", 18, 100, 30)
    sex = st.radio("🚻 الجنس", ["ذكر", "أنثى"])
    cp = st.selectbox("💓 نوع ألم الصدر", [0, 1, 2, 3])
    trtbps = st.slider("🩸 ضغط الدم الانقباضي (mm Hg)", 80, 200, 120)
    chol = st.slider("🥓 الكوليسترول (mg/dl)", 100, 600, 200)
    fbs = st.radio("🍬 سكر صائم > 120 mg/dl", [0, 1])
    restecg = st.selectbox("📈 نتائج تخطيط القلب", [0, 1, 2])
    thalachh = st.slider("❤️ أقصى معدل ضربات القلب", 60, 220, 150)
    exng = st.radio("🏃‍♂️ ألم الصدر عند المجهود", [0, 1])
    oldpeak = st.slider("📉 انخفاض ST", 0.0, 10.0, 1.0)
    slp = st.selectbox("📊 ميل مقطع ST", [0, 1, 2])
    caa = st.selectbox("🩸 عدد الأوعية الرئيسية", [0, 1, 2, 3, 4])
    thall = st.selectbox("🧬 نوع الثلاسيميا", [0, 1, 2, 3])

    sex_val = 1 if sex == "ذكر" else 0

    features = np.array([[age, sex_val, cp, trtbps, chol, fbs,
                          restecg, thalachh, exng, oldpeak, slp,
                          caa, thall]])

    if st.button("🔍 تنبؤ"):
        with st.spinner("جاري تحليل البيانات..."):
            prediction = model.predict(features)
            risk_proba = model.predict_proba(features)[0][1] * 100  # نسبة الخطر
            st.session_state.prediction = prediction[0]
            st.session_state.risk_value = risk_proba
            st.session_state.page = "result"

# صفحة عرض النتيجة
elif st.session_state.page == "result":
    st.header(f"📊 نتيجة التنبؤ للمستخدم {st.session_state.username}")

    risk_value = st.session_state.risk_value
    if st.session_state.prediction == 1:
        st.error(f"⚠️ هناك احتمال لإصابتك بمرض القلب.\n💔 نسبة الخطر: {risk_value:.1f}%")
        color = "red"
        advice = """
        - 🥗 تناول غذاء صحي قليل الدهون والملح  
        - 🏃‍♀️ مارس الرياضة بانتظام  
        - 🚭 توقف عن التدخين  
        - 🩺 راقب ضغط الدم والسكر  
        - 😌 تجنب التوتر  
        - 🩹 راجع الطبيب دوريًا
        """
    else:
        st.success(f"✅ لا توجد مؤشرات قوية على مرض القلب.\n💚 نسبة الخطر: {risk_value:.1f}%")
        color = "green"
        advice = """
        - 🥗 استمر في نمط حياة صحي  
        - 🚶 مارس المشي أو الرياضة الخفيفة  
        - ⚖️ حافظ على وزن مثالي  
        - 🛌 نم جيدًا  
        - 🩺 تابع فحوصاتك الدورية
        """

    # عرض نصائح طبية
    with st.expander("🩺 نصائح"):
        st.markdown(advice)

    # رسم نسبة الخطر باستخدام Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_value,
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "#c6f5d9"},
                {'range': [30, 70], 'color': "#fff2cc"},
                {'range': [70, 100], 'color': "#f4c7c3"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_value
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🔄 العودة"):
        st.session_state.page = "form"
