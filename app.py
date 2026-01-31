import streamlit as st
from openai import OpenAI
import os
import time

st.set_page_config(page_title="献立提案AI", page_icon="🍽️")

st.title("献立提案アプリ 🍽️")

# APIキー読み込み
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY が設定されていません")
    st.stop()

client = OpenAI(api_key=api_key)

# 入力フォーム
with st.form("menu_form"):
    用途 = st.text_input("用途（例：晩ご飯、弁当）")
    日数 = st.number_input("日数", 1, 7, 3)
    食材 = st.text_input("使いたい食材（任意）")
    制限 = st.text_input("アレルギー・苦手食材（任意）")
    要望 = st.text_input("要望（簡単・節約など）")

    submitted = st.form_submit_button("献立を提案する")

if submitted:
    prompt = f"""
あなたは管理栄養士です。
以下条件で{日数}日分の献立と食材を提案してください。

用途：{用途}
食材：{食材 or "なし"}
制限：{制限 or "なし"}
要望：{要望 or "なし"}

出力形式：
1. 日ごとの献立
2. レシピ概要
3. 必要な食材まとめ
"""

    with st.spinner("献立を生成中...🍳"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )

            st.subheader("📋 提案結果")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error("API制限または課金未設定の可能性があります")
            st.write("詳細：", e)
