# https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet
# https://medium.com/@preveenraj/image-upload-to-firebase-storage-with-python-ebf18c615f34
import os
import time
import uuid
import base64
import streamlit as st
from google.cloud import firestore, storage
from google.oauth2 import service_account
from google.auth.transport import mtls
from PIL import Image
from datetime import datetime


db = firestore.Client.from_service_account_json(".firestore-key.json")
storage_client = storage.Client.from_service_account_json(".gcs-key.json")
# bucket_name = "anita-40-anniversary-test"
bucket_name = "anita-40-anniversary-prod"

# confirm local folder exists
_directory_ = '/home/ubuntu/anita_photo/' + \
        datetime.today().strftime('%Y_%m_%d')
bucket = storage_client.get_bucket(bucket_name)
if not os.path.exists(_directory_):
    os.makedirs(_directory_)

# 網頁配置設定
st.set_page_config(
    page_title="Anita Mui 出道 40 週年應援活動",
    page_icon="🎤",
   layout="wide",
    initial_sidebar_state="collapsed")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# # 加入進度條, 增加一個空白元件，等等要放文字
# latest_iteration = st.empty()
# bar = st.progress(0)
# for i in range(100):
# 	latest_iteration.text(f"目前進度: {i+1} %")
# 	bar.progress(i + 1)
# 	time.sleep(0.1)


st.markdown("<h1 style='text-align: center; color: black;'>梅艷芳出道四十週年紀念晝展</h1>",
            unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>未變情懷40載, 流年似水如一夢</h2>",
            unsafe_allow_html=True)


def load_image(image_file):
    img = Image.open(image_file)
    return img


# Streamlit widgets to let a user create a new post
unique_id = str(uuid.uuid1())
today = st.date_input("今天日期")
nickname = st.text_input("暱稱:")
image_file = st.file_uploader(
    "先讓我們為今天留下美好的紀念吧！放張你最喜歡的 Anita 或是為今天留下一個紀念吧！ P.S.可以上傳多張照片唷！", accept_multiple_files=True)
place = st.text_input("hello! 請問你是來自哪裡的粉絲:")
years = st.text_input(f"想請問一下，你喜歡 Anita 已經有幾年了？")
sentence = st.text_area(f"那麽你最想對 Anita 說什麼呢？", height=100)

st.markdown("<h4 style='text-align: center; color: black;'>讓我們來看看今天留下的回憶吧！</h4>",
            unsafe_allow_html=True)
# display uploaded images
if image_file is not None:
    # To View Uploaded Image
    if image_file != []:
        if len(image_file) > 2:
            img_list = [load_image(image) for image in image_file]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(img_list[0], width=300, use_column_width='Ture')
            with col2:
                st.image(img_list[1], width=300, use_column_width='Ture')
            with col3:
                st.image(img_list[2], width=300, use_column_width='Ture')

        elif len(image_file) == 2:
            img_list = [load_image(image) for image in image_file]
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write(' ')
            with col2:
                st.image(img_list[0], width=300, use_column_width='Ture')
            with col3:
                st.write(' ')
            with col4:
                st.image(img_list[1], width=300, use_column_width='Ture')
            with col5:
                st.write(' ')

        else:
            img_list = [load_image(image) for image in image_file]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(' ')
            with col2:
                st.image(img_list[0], width=300, use_column_width='Ture')
            with col3:
                st.write(' ')
# # Once the user has submitted, upload it to the Firebase database
# if nickname and place and years and sentence and image_file is not None:
#     doc_ref = db.collection("anita-40-anniversary").document(unique_id)
#     doc_ref.set({
#         "uuid": unique_id,
#         "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "nickname": nickname,
#         "place": place,
#         "year": years,
#         "sentence": sentence
#     })

#     for image in image_file:
#         local_fileName = unique_id + '-' + image.name
#         gcs_fileName = unique_id + '/' + image.name

#         with open(os.path.join(_directory_, local_fileName), "wb") as f:
#             f.write(image.getbuffer())

#         # upload image to GCS
#         blob = bucket.blob(gcs_fileName)
#         blob.upload_from_filename(os.path.join(_directory_, local_fileName))
    

# # Once the user has submitted, upload it to the Firebase database
# if nickname and place and years and sentence:
#     doc_ref = db.collection("anita").document(unique_id)
#     doc_ref.set({
#         "uuid": unique_id,
#         "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "nickname": nickname,
#         "place": place,
#         "year": years,
#         "sentence": sentence
#     })
#     st.subheader(
#         f"我們收到囉! 我們會將你們想對 Anita 說的話整理起來，一切消息都會公佈在小海 Instagram 帳號! 敬請期待 😆")

# if image_file is not None:
#     # save image to local
#     for image in image_file:
#         local_fileName = unique_id + '-' + image.name
#         gcs_fileName = unique_id + '/' + image.name

#         with open(os.path.join(_directory_, local_fileName), "wb") as f:
#             f.write(image.getbuffer())

#         # upload image to GCS
#         blob = bucket.blob(gcs_fileName)
#         blob.upload_from_filename(os.path.join(_directory_, local_fileName))


# Once the user has submitted, upload it to the Firebase database
if nickname and place and years and sentence and image_file is not None:
    doc_ref = db.collection("anita-40-anniversary").document(unique_id)
    doc_ref.set({
        "uuid": unique_id,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nickname": nickname,
        "place": place,
        "year": years,
        "sentence": sentence
    })

    for image in image_file:
        local_fileName = unique_id + '-' + image.name
        gcs_fileName = unique_id + '/' + image.name

        with open(os.path.join(_directory_, local_fileName), "wb") as f:
            f.write(image.getbuffer())

        # upload image to GCS
        blob = bucket.blob(gcs_fileName)
        blob.upload_from_filename(os.path.join(_directory_, local_fileName))
    
st.subheader(
        f"你們想對 Anita 說的話我們已經收到囉! 我們會將這些寶貝整理起來，一切消息都會公佈在小海 Instagram 帳號! 敬請期待 😆")

st.markdown("<h2 style='text-align: center; color: black;'>謝謝今天的拜訪，你填寫的小卡之後會製作成驚喜唷！</h2>",
            unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>一切消息都會公佈在小海的 <a href='https://www.instagram.com/paintinglife_0707/'>Instagram 帳號</a> 敬請期待 😆</h2>", unsafe_allow_html=True)

# # display anita youtube music
# # st.video("https://www.youtube.com/watch?v=EoTMlRISRuQ", start_time=0)

# https://github.com/soft-nougat/streamlitwebcam/tree/main/final_model
# https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067/9
# https://vocus.cc/article/60ea6520fd89780001771fcd

# 背景、自動播歌、寫資料進 firestore、寫照片進 firestore/GCS

# # debug:
# 1. MemoryError: Cannot allocate write+execute memory for ffi.callback().
# https://github.com/pyca/pyopenssl/issues/873 | pip3 uninstall pyopenssl
# 2. No module named 'Crypto'的解决方案
# https://segmentfault.com/a/1190000039335378


# sudo apt-get update
# sudo apt-get -y install python3-pip
# pip3 --version

# nano requirements.txt
# streamlit
# google-cloud-firestore
# Pillow
# PyDrive
# gsheetsdb==0.1.13

# pip install -r requirements.txt

# nano streamlit_app.py
#     import time
#     import streamlit as st

#     import numpy as np
#     import pandas as pd
#     st.title('我的第一個應用程式')

# export PATH="$HOME/.local/bin:$PATH"
# streamlit run streamlit_app.py

# # setup timezone
# sudo timedatectl set-timezone Asia/Hong_Kong
