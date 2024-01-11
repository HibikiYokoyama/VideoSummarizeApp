# 動画の内容要約アプリ
## 概要
アップロードされた動画の音声を文字起こしし、その要約を出力する。

Webアプリの作成にはPythonフレームワークのStreamlitを使用。

## 実行画面
- アップロードされた音声付き動画の内容の要約を出力
> デモ動画には[【ライブ】お昼のニュース 1月11日〈FNNプライムオンライン〉](https://www.youtube.com/live/D6GfaCXzFFQ?si=e9Zwf5Imlaj6MSmH&t=2677)を使用
<img src="https://github.com/HibikiYokoyama/VideoSummarizeApp/assets/89569080/a3c50675-71b4-4844-9cb2-87d2647cbc79" width="800">

## 各コードの概要
- **run_app.py**  
-アプリ実行用プログラム

## 要約モデルの訓練に使用したデータセット
-  **ThreeLineSummaryDataset（<https://github.com/KodairaTomonori/ThreeLineSummaryDataset>）** の一部をスクレイピングして使用

## 使用ライブラリ
- **streamlit 1.29.0**
- **speechrecognition 3.10.1**
- **moviepy 1.0.3**
- **transformers 4.36.2**
- **torch 2.1.2**
- **sentencepiece 0.1.99**

## 実行コマンド
```bash
streamlit run run_app.py
```
