import time
import streamlit as st

st.set_page_config(page_title="インターネットのしくみ たいけん", page_icon="🌐", layout="centered")

# ---------- セッション状態の初期化 ----------
if "stage" not in st.session_state:
    st.session_state.stage = 0          # 0:見たいもの入力 1:URL入力 2:通信中演出 3:完了
if "want" not in st.session_state:
    st.session_state.want = ""
if "url" not in st.session_state:
    st.session_state.url = ""
if "shown_steps" not in st.session_state:
    st.session_state.shown_steps = 0    # 演出のどこまで表示したか

IP_ADDRESS = "123.45.67.89"

st.title("🌐 インターネットのしくみ たいけん")
st.caption("Webページが表示されるまでの流れを、じぶんで体験してみよう。")

st.divider()

# これまでの入力を常に表示（あれば）
if st.session_state.want:
    st.write(f"👀 あなたが見たいもの：**{st.session_state.want}**")
if st.session_state.url:
    st.write(f"🔗 かいたアドレス：`{st.session_state.url}`")

st.divider()

# ---------- ステージ0：見たいものを言葉で入力 ----------
if st.session_state.stage == 0:
    want = st.text_input(
        "あなたが見たいものは何ですか。言葉でかいてください",
        value=st.session_state.want,
        placeholder="例：かわいい ねこ の しゃしん",
    )
    if st.button("つぎへ ➡️", disabled=(want.strip() == "")):
        st.session_state.want = want.strip()
        st.session_state.stage = 1
        st.rerun()

# ---------- ステージ1：URLを入力 ----------
elif st.session_state.stage == 1:
    url = st.text_input(
        "では、https:// ・・・　でかいてください",
        value=st.session_state.url if st.session_state.url else "https://",
    )
    ready = url.strip() not in ("", "https://")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ もどる"):
            st.session_state.stage = 0
            st.rerun()
    with col2:
        if st.button("けんさく 🔍", disabled=not ready):
            st.session_state.url = url.strip()
            st.session_state.stage = 2
            st.session_state.shown_steps = 0
            st.rerun()

# ---------- ステージ2：通信の演出 ----------
elif st.session_state.stage == 2:
    steps = [
        ("🛰️", "DNSサーバーに問い合わせております。"),
        ("📮", f"みつかりました。あなたに（{IP_ADDRESS}）を送ります。\n自動です。"),
        ("📡", "受けとったアドレスをWebサーバーに送ります。\n自動です。"),
        ("📄", f"Webサーバーがページを開いて届けてくれました。自動です。\nあなたがみたいもの、「{st.session_state.want}」ですか？"),
    ]

    placeholder = st.container()

    # まだ表示していないステップを1つずつ、少し待ってから表示していく
    if st.session_state.shown_steps < len(steps):
        with placeholder:
            for i in range(st.session_state.shown_steps):
                icon, text = steps[i]
                st.success(f"{icon} {text}")
            icon, text = steps[st.session_state.shown_steps]
            with st.spinner(f"{icon} {text}"):
                time.sleep(1.6)
        st.session_state.shown_steps += 1
        st.rerun()
    else:
        with placeholder:
            for icon, text in steps:
                st.success(f"{icon} {text}")
        st.session_state.stage = 3
        st.rerun()

# ---------- ステージ3：完了 ----------
elif st.session_state.stage == 3:
    steps = [
        ("🛰️", "DNSサーバーに問い合わせております。"),
        ("📮", f"みつかりました。あなたに（{IP_ADDRESS}）を送ります。\n自動です。"),
        ("📡", "受けとったアドレスをWebサーバーに送ります。\n自動です。"),
        ("📄", f"Webサーバーがページを開いて届けてくれました。自動です。\nあなたがみたいもの、「{st.session_state.want}」ですか？"),
    ]
    for icon, text in steps:
        st.success(f"{icon} {text}")

    st.balloons()
    if st.button("🔄 もういちど さいしょから"):
        st.session_state.stage = 0
        st.session_state.want = ""
        st.session_state.url = ""
        st.session_state.shown_steps = 0
        st.rerun()