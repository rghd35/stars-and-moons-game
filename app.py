
import streamlit as st
import random

st.set_page_config(
    page_title="لعبة نجوم وأقمار",
    page_icon="🌟",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #111827, #302052);
    color: white;
}
h1, h2, h3, p {
    text-align: center;
}
.stButton > button {
    background: #7855d9;
    color: white;
    border-radius: 12px;
    border: none;
    width: 100%;
    padding: 12px;
    font-weight: bold;
}
.stButton > button:hover {
    background: #9b7af5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# إعداد حالة اللعبة
defaults = {
    "page": "home",
    "players": [],
    "secret": "",
    "turn": 0,
    "attempts": 0,
    "max_attempts": 10,
    "history": [],
    "winner": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def generate_secret():
    # أربعة أرقام مختلفة، ويمكن أن يبدأ العدد بصفر
    return "".join(random.sample("0123456789", 4))


def evaluate_guess(secret, guess):
    stars = sum(
        secret[i] == guess[i]
        for i in range(4)
    )

    moons = sum(
        digit in secret for digit in guess
    ) - stars

    return stars, moons


def valid_guess(guess):
    if len(guess) != 4:
        return False, "يجب إدخال 4 أرقام بالضبط."

    if not guess.isdigit():
        return False, "يُسمح بالأرقام فقط."

    if len(set(guess)) != 4:
        return False, "يجب ألا تتكرر الأرقام."

    return True, ""


def start_game(names):
    st.session_state.players = names
    st.session_state.secret = generate_secret()
    st.session_state.turn = 0
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.winner = None
    st.session_state.page = "game"


def restart():
    st.session_state.secret = generate_secret()
    st.session_state.turn = 0
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.winner = None
    st.session_state.page = "game"


st.title("🌟 لعبة نجوم وأقمار 🌙")
st.markdown("---")

# الصفحة الرئيسية
if st.session_state.page == "home":

    st.header("أهلًا بكم في اللعبة!")
    st.write("اختبروا ذكاءكم في تخمين الرقم السري.")

    st.subheader("📖 تعليمات اللعبة")

    st.info("""
    🎯 الهدف: تخمين الرقم السري المكوّن من 4 أرقام.

    ⭐ نجمة: رقم صحيح وفي المكان الصحيح.

    🌙 قمر: رقم صحيح ولكن في مكان خاطئ.

    ❌ لا شيء: الرقم غير موجود في العدد السري.

    🔟 الحد الأقصى 10 محاولات.

    🏆 يفوز اللاعب الذي يخمّن الرقم كاملًا.
    """)

    number_players = st.radio(
        "اختاروا عدد اللاعبين:",
        [1, 2],
        horizontal=True
    )

    names = []

    for i in range(number_players):
        name = st.text_input(
            f"اسم اللاعب {i + 1}",
            key=f"player_{i}"
        )
        names.append(name.strip())

    if st.button("🚀 ابدأ اللعبة"):
        if all(names):
            start_game(names)
            st.rerun()
        else:
            st.warning("الرجاء إدخال أسماء جميع اللاعبين.")

# صفحة اللعب
elif st.session_state.page == "game":

    player = st.session_state.players[
        st.session_state.turn
    ]

    remaining = (
        st.session_state.max_attempts
        - st.session_state.attempts
    )

    st.subheader(f"🎮 دور اللاعب: {player}")

    st.metric("المحاولات المتبقية", remaining)

    st.progress(
        st.session_state.attempts /
        st.session_state.max_attempts
    )

    st.write("أدخل رقمًا مكونًا من 4 خانات مختلفة.")

    with st.form("guess_form", clear_on_submit=True):
        guess = st.text_input(
            "الرقم المتوقع:",
            max_chars=4,
            placeholder="مثال: 1234"
        )

        submitted = st.form_submit_button(
            "🔍 تحقق من التخمين"
        )

    if submitted:
        is_valid, message = valid_guess(guess)

        if not is_valid:
            st.error(message)

        else:
            stars, moons = evaluate_guess(
                st.session_state.secret,
                guess
            )

            st.session_state.attempts += 1

            st.session_state.history.append({
                "اللاعب": player,
                "التخمين": guess,
                "النجوم ⭐": stars,
                "الأقمار 🌙": moons
            })

            if stars == 4:
                st.session_state.winner = player
                st.session_state.page = "result"

            elif (
                st.session_state.attempts
                >= st.session_state.max_attempts
            ):
                st.session_state.page = "result"

            else:
                st.session_state.turn = (
                    st.session_state.turn + 1
                ) % len(st.session_state.players)

            st.rerun()

    st.subheader("📜 سجل التخمينات")

    if st.session_state.history:
        st.dataframe(
            st.session_state.history,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("لم يتم إدخال أي تخمين بعد.")

    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()

# صفحة النتيجة
elif st.session_state.page == "result":

    if st.session_state.winner:
        st.balloons()

        st.success(
            f"🏆 مبروك {st.session_state.winner}!"
        )

        st.header("لقد فزت باللعبة! 🎉")

    else:
        st.error("انتهت المحاولات! 😢")
        st.header("حظًا أوفر في المرة القادمة!")

    st.subheader(
        f"🔐 الرقم السري كان: "
        f"{st.session_state.secret}"
    )

    st.write(
        f"عدد المحاولات المستخدمة: "
        f"{st.session_state.attempts}"
    )

    st.subheader("📊 النتائج النهائية")

    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🔄 العب مرة أخرى"):
        restart()
        st.rerun()

    if st.button("🏠 الصفحة الرئيسية"):
        st.session_state.page = "home"
        st.rerun()
