import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# =========================
# 環境変数の読み込み
# =========================
load_dotenv()

# =========================
# 画面の基本設定
# =========================
st.set_page_config(
    page_title="専門家に相談できるLLMアプリ",
    page_icon="🤖",
    layout="centered"
)

# =========================
# アプリ概要
# =========================
st.title("🤖 専門家に相談できるLLMアプリ")
st.write(
    """
このアプリでは、入力した質問に対して、選択した専門家の立場でLLMが回答します。

### 使い方
1. ラジオボタンで専門家の種類を選択してください。
2. 入力フォームに質問や相談内容を入力してください。
3. 「送信」ボタンを押すと、回答が表示されます。
"""
)

# =========================
# APIキー取得
# ローカル: .env
# デプロイ後: Streamlit Secrets
# =========================
# APIキー取得（ローカル実行用）
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY が設定されていません。.env を確認してください。")
    st.stop()

# =========================
# LLM回答関数
# =========================
def get_llm_response(user_text: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類を受け取り、
    LLMからの回答を文字列で返す関数
    """

    # 専門家の種類に応じてシステムメッセージを切り替える
    if expert_type == "A: Python学習の専門家":
        system_prompt = (
            "あなたはPython学習を支援する専門家です。"
            "初心者にも分かりやすく、丁寧で実用的に説明してください。"
            "必要に応じて具体例も交えてください。"
        )
    elif expert_type == "B: 業務改善の専門家":
        system_prompt = (
            "あなたは業務改善の専門家です。"
            "現場で実行しやすい改善案を、論理的かつ実務的に提案してください。"
            "必要に応じて手順や優先順位も示してください。"
        )
    else:
        system_prompt = "あなたは親切で有能なアシスタントです。"

    # Lesson8 の形を踏まえて LangChain でメッセージ作成
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text),
    ]

    # LLM準備
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key
    )

    # 回答生成
    result = llm.invoke(messages)

    return result.content

# =========================
# 入力UI
# =========================
expert_type = st.radio(
    "専門家の種類を選択してください",
    ("A: Python学習の専門家", "B: 業務改善の専門家")
)

user_text = st.text_area(
    "質問・相談内容を入力してください",
    height=180,
    placeholder="例：Pythonで関数の作り方を教えてください。"
)

# =========================
# 実行ボタン
# =========================
if st.button("送信"):
    if not user_text.strip():
        st.warning("入力テキストを入力してください。")
    else:
        with st.spinner("LLMが回答を作成中です..."):
            try:
                answer = get_llm_response(user_text, expert_type)

                st.subheader("回答結果")
                st.write(answer)

            except Exception as e:
                st.error("エラーが発生しました。詳細は以下です。")
                st.exception(e)