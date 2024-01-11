import streamlit as st
from transformers.models.t5 import T5ForConditionalGeneration
from transformers import T5Tokenizer
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import tempfile
import re
import time

# 追加訓練済みT5とトークナイザの読み込み
t5_model = T5ForConditionalGeneration.from_pretrained('./models')
t5_tokenizer = T5Tokenizer.from_pretrained('sonoisa/t5-base-japanese', legacy=False)
t5_model.eval()

# 音声を抽出し、文字起こしを行う関数
def extract_and_transcribe(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        video_file_path = temp_video.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio_path = temp_audio.name

    videoclip = VideoFileClip(video_file_path)
    audioclip = videoclip.audio
    audioclip.write_audiofile(audio_path)
    audioclip.close()
    videoclip.close()

    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="ja-JP")
        return text

# テキストを要約する関数
def summarize_text(text):
    tokens = t5_tokenizer.encode("summarize: " + text, add_special_tokens=False)
    inputs = t5_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = t5_model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    s_list = re.split(r'(?<=。)', summary)
    dup_chk = set()
    summary_text = [s for s in s_list if s and (s not in dup_chk) and not dup_chk.add(s)]
    if summary_text and summary_text[-1][-1] != '。':
        summary_text.pop()

    return summary_text

# Streamlit UIの設定
st.title('動画の内容要約アプリ')

# 動画アップロード
uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4"])
if uploaded_file is not None:
    st.video(uploaded_file)
    
    # 進捗とステータスメッセージ
    progress_bar = st.progress(0)
    status_message = st.empty()
    status_message.text("音声の文字起こしを行っています...")

    try:
        # 文字起こし
        transcribed_text = extract_and_transcribe(uploaded_file)
        progress_bar.progress(50)
        status_message.text("要約を行っています...")

        # 要約
        summary_text = summarize_text(transcribed_text)
        progress_bar.progress(100)
        time.sleep(0.5)
        status_message.empty()

        st.write("要約結果:")
        st.write(*summary_text)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    progress_bar.empty()
    status_message.empty()
