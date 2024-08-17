import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# 設置頁面配置
st.set_page_config(page_title="Image Creator for Family", layout="wide")

# OpenAI API 設置
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai_api_url = "https://api.openai.com/v1/images/generations"

# LINE Notify 設置
line_notify_token = st.secrets["LINE_NOTIFY_TOKEN"]
line_notify_api = "https://notify-api.line.me/api/notify"

def generate_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post(openai_api_url, headers=headers, json=data)
    return response.json()["data"][0]["url"]

def send_line_notify(message, image_url):
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    data = {
        "message": message,
        "imageThumbnail": image_url,
        "imageFullsize": image_url
    }
    requests.post(line_notify_api, headers=headers, data=data)

# Streamlit UI
st.title("Image Creator for Family & LINE Notify to the group")

# 用戶輸入
prompt = st.text_input("請輸入圖片描述(Please Input Picture Description)：")

if st.button("生成圖片(Generate Pics)"):
    if prompt:
        with st.spinner("正在生成圖片(Generating)..."):
            image_url = generate_image(prompt)
            st.session_state["current_image"] = image_url
            st.success("圖片生成成功(Successs)！")
    else:
        st.warning("請輸入圖片描述(Please Input Picture Description)。")

# 顯示生成的圖片
if "current_image" in st.session_state:
    st.image(st.session_state["current_image"], caption="生成的圖片(Picture Generated)", use_column_width=True)
    
    # 添加發送到LINE的按鈕
    if st.button("發送到LINE"):
        with st.spinner("正在發送到LINE..."):
            send_line_notify(f"新生成的圖片\n描述: {prompt}", st.session_state["current_image"])
            st.success("圖片已成功發送到LINE！")

    # 添加重新生成的按鈕
    if st.button("重新生成(Re-Generating"):
        st.session_state.pop("current_image", None)
        st.experimental_rerun()

# 添加說明
st.markdown("""
### 使用說明：
1. 在文本框中輸入你想要生成的圖片描述。
2. 點擊"生成圖片"按鈕來創建圖片。
3. 如果你不滿意生成的圖片，可以點擊"重新生成"按鈕。
4. 當你對圖片滿意時，點擊"發送到LINE"按鈕將圖片發送到你的LINE。
""")
