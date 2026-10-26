
import random
import html
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="نجوم وأقمار | Stars & Moons",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# RESPONSIVE SKY BLUE DESIGN
# ==========================================

st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(
        180deg,
        #dff3ff 0%,
        #f1faff 50%,
        #fff9e9 100%
    );
}

/* Main container */
.block-container {
    max-width: 740px;
    padding: 1.2rem 1rem 3rem;
}

/* Typography */
h1, h2, h3 {
    color: #24577d !important;
    text-align: center;
}

p, label {
    color: #345c7c;
}

/* Header */
.hero {
    text-align: center;
    padding: 22px 12px;
    background: rgba(255,255,255,0.75);
    border: 1px solid #c9e8fa;
    border-radius: 24px;
    margin-bottom: 20px;
}

.hero-title {
    color: #25618e;
    font-size: 35px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #6587a0;
    font-size: 16px;
}

/* Cards */
.game-card {
    background: white;
    padding: 20px;
    border: 1px solid #cde9f8;
    border-radius: 20px;
    text-align: center;
    margin: 12px 0;
    box-shadow: 0 5px 20px rgba(72,145,192,0.08);
}

.card-title {
    font-size: 21px;
    font-weight: 750;
    color: #24577d;
    margin-bottom: 8px;
}

.card-text {
    color: #6587a0;
    font-size: 15px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(
        90deg,
        #369fdf,
        #659ff0
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    min-height: 49px;
    font-weight: 700;
    width: 100%;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #2787c8 !important;
}

/* Text inputs */
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    color: #24577d !important;
    border: 1.5px solid #b9def4 !important;
    border-radius: 12px !important;
    min-height: 45px;
}

/* Number inputs */
.digit-input input {
    text-align: center;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #cde9f8;
    border-radius: 16px;
    padding: 12px;
    text-align: center;
}

div[data-testid="stMetric"] * {
    color: #24577d !important;
}

/* Results */
.feedback {
    background: #e7f5ff;
    border: 1px solid #b6e1fa;
    border-radius: 17px;
    padding: 18px;
    text-align: center;
    color: #24577d;
    margin: 15px 0;
}

.feedback-title {
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 10px;
}

.feedback-score {
    font-size: 23px;
    font-weight: 800;
}

/* Secret number */
.secret-digit {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 54px;
    height: 62px;
    margin: 3px;
    background: white;
    border: 2px solid #8bcaf0;
    border-radius: 14px;
    font-size: 28px;
    font-weight: 800;
    color: #287ab3;
}

/* Mobile responsive layout */
@media (max-width: 600px) {

    .block-container {
        padding: 0.8rem 0.65rem 2rem;
    }

    .hero {
        padding: 18px 10px;
        border-radius: 18px;
    }

    .hero-title {
        font-size: 27px;
    }

    .hero-subtitle {
        font-size: 13px;
    }

    .game-card {
        padding: 15px 10px;
    }

    .card-title {
        font-size: 19px;
    }

    .secret-digit {
        width: 45px;
        height: 54px;
        font-size: 24px;
    }

    div[data-testid="stTextInput"] input {
        font-size: 16px;
        padding: 7px;
    }

    .feedback-score {
        font-size: 21px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 48px;
        font-size: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# GAME STATE
# ==========================================

defaults = {
    "started": False,
    "players": [],
    "secret": "",
    "turn": 0,
    "attempts": 0,
    "max_attempts": 10,
    "history": [],
    "winner": None,
    "game_over": False,
    "last_result": None,
    "game_id": 0,
    "player_count": 1,
    "player_name_0": "",
    "player_name_1": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# GAME FUNCTIONS
# ==========================================

def generate_secret():
    """Generate four unique random digits."""
    return "".join(random.sample("0123456789", 4))


def validate_guess(guess):
    """Validate the player's guess."""

    if len(guess) != 4:
        return False, "يجب إدخال 4 أرقام بالضبط."

    if not guess.isascii() or not guess.isdigit():
        return False, "الرجاء إدخال أرقام من 0 إلى 9."

    if len(set(guess)) != 4:
        return False, "لا يمكن تكرار نفس الرقم."

    return True, ""


def calculate_result(secret, guess):
    """Calculate stars and moons."""

    stars = 0
    moons = 0

    for i in range(4):
        if guess[i] == secret[i]:
            stars += 1
        elif guess[i] in secret:
            moons += 1

    return stars, moons


def start_game():
    count = st.session_state.player_count

    names = [
        st.session_state[f"player_name_{i}"].strip()
        for i in range(count)
    ]

    if not all(names):
        st.error("الرجاء إدخال أسماء جميع اللاعبين.")
        return

    if len(set(names)) != len(names):
        st.error("يجب أن تكون أسماء اللاعبين مختلفة.")
        return

    st.session_state.players = names
    st.session_state.secret = generate_secret()
    st.session_state.turn = 0
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.last_result = None
    st.session_state.started = True
    st.session_state.game_id += 1

    st.rerun()


def play_again():
    st.session_state.secret = generate_secret()
    st.session_state.turn = 0
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.last_result = None
    st.session_state.game_id += 1
    st.rerun()


def change_players():
    st.session_state.started = False
    st.session_state.game_over = False
    st.session_state.last_result = None
    st.rerun()


def submit_guess(guess):
    """Process a player's guess."""

    valid, message = validate_guess(guess)

    if not valid:
        st.error(message)
        return

    player = st.session_state.players[
        st.session_state.turn
    ]

    stars, moons = calculate_result(
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

    st.session_state.last_result = {
        "player": player,
        "guess": guess,
        "stars": stars,
        "moons": moons
    }

    if stars == 4:
        st.session_state.winner = player
        st.session_state.game_over = True

    elif (
        st.session_state.attempts
        >= st.session_state.max_attempts
    ):
        st.session_state.game_over = True

    else:
        st.session_state.turn = (
            st.session_state.turn + 1
        ) % len(st.session_state.players)

    st.rerun()


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        ☁️ نجوم وأقمار 🌙
    </div>
    <div class="hero-subtitle">
        اكتشف الرقم السري واجمع النجوم للفوز! ⭐
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# PLAYER SETUP
# ==========================================

st.markdown("### 👥 اللاعبين")

if not st.session_state.started:

    st.radio(
        "كم لاعب رح يلعب؟",
        options=[1, 2],
        horizontal=True,
        key="player_count",
        format_func=lambda x: (
            "لاعب واحد" if x == 1 else "لاعبان"
        )
    )

    for i in range(st.session_state.player_count):
        st.text_input(
            f"اسم اللاعب {i + 1}",
            key=f"player_name_{i}",
            placeholder="اكتب الاسم هنا"
        )

    if st.button(
        "🚀 ابدأ اللعب",
        use_container_width=True
    ):
        start_game()

else:

    names_text = " | ".join(
        html.escape(name)
        for name in st.session_state.players
    )

    st.markdown(
        f"""
        <div class="game-card">
            <div class="card-title">
                🎮 اللاعبون
            </div>
            <div class="card-text">
                {names_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================================
    # GAME SECTION
    # ======================================

    if not st.session_state.game_over:

        player = st.session_state.players[
            st.session_state.turn
        ]

        st.markdown(
            f"""
            <div class="game-card">
                <div class="card-title">
                    ⭐ دور اللاعب:
                    {html.escape(player)}
                </div>
                <div class="card-text">
                    خمن الرمز المكون من 4 أرقام
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "المحاولات المستخدمة",
                st.session_state.attempts
            )

        with col2:
            st.metric(
                "المحاولات المتبقية",
                st.session_state.max_attempts
                - st.session_state.attempts
            )

        st.progress(
            st.session_state.attempts /
            st.session_state.max_attempts
        )

        st.markdown("### 🔢 أدخل تخمينك")

        # Four responsive digit inputs
        with st.form(
            key=f"guess_form_{st.session_state.game_id}",
            clear_on_submit=True
        ):

            columns = st.columns(
                4,
                gap="small"
            )

            digits = []

            for i in range(4):

                with columns[i]:
                    digit = st.text_input(
                        f"رقم {i + 1}",
                        max_chars=1,
                        key=(
                            f"digit_{st.session_state.game_id}_{i}"
                        ),
                        placeholder="0"
                    )
                    digits.append(digit)

            submitted = st.form_submit_button(
                "⭐ تحقق من التخمين 🌙",
                use_container_width=True
            )

        if submitted:
            guess = "".join(digits)
            submit_guess(guess)

        # Last result
        if st.session_state.last_result:

            result = st.session_state.last_result

            st.markdown(
                f"""
                <div class="feedback">
                    <div class="feedback-title">
                        ✨ نتيجة آخر تخمين
                    </div>
                    <div>
                        🔢 {result['guess']}
                    </div>
                    <div class="feedback-score">
                        ⭐ {result['stars']}
                        &nbsp;&nbsp;
                        🌙 {result['moons']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ======================================
    # GAME RESULT
    # ======================================

    if st.session_state.game_over:

        if st.session_state.winner:

            st.balloons()

            st.success(
                f"🏆 مبروك {st.session_state.winner}!"
            )

            st.markdown("""
            <div class="game-card">
                <div class="card-title">
                    🎉 لقد فزت!
                </div>
                <div class="card-text">
                    حصلت على 4 نجوم واكتشفت
                    الرقم السري بنجاح!
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.error("🌧️ انتهت المحاولات!")

            st.markdown("""
            <div class="game-card">
                <div class="card-title">
                    حظًا أوفر في المرة القادمة!
                </div>
                <div class="card-text">
                    لم يتم اكتشاف الرقم السري.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🔐 الرقم السري")

        secret_digits = "".join(
            f'<span class="secret-digit">{d}</span>'
            for d in st.session_state.secret
        )

        st.markdown(
            f"""
            <div style="text-align:center;">
                {secret_digits}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.metric(
            "عدد المحاولات المستخدمة",
            st.session_state.attempts
        )

        if st.button(
            "🔄 العب مرة أخرى",
            use_container_width=True
        ):
            play_again()

    # ======================================
    # GUESS HISTORY
    # ======================================

    st.markdown("### 📜 سجل المحاولات")

    if st.session_state.history:

        st.dataframe(
            st.session_state.history,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "لم يتم إدخال أي تخمين حتى الآن."
        )

    if st.button(
        "👥 تغيير اللاعبين",
        use_container_width=True
    ):
        change_players()


# ==========================================
# INSTRUCTIONS - BOTTOM OF PAGE
# ==========================================

st.divider()

st.markdown("### 📖 تعليمات اللعبة")

with st.expander(
    "🌟 اضغط هنا لقراءة طريقة اللعب",
    expanded=True
):

    st.markdown("""
    **🎯 هدف اللعبة**

    اكتشاف الرقم السري المكوّن من
    أربعة أرقام مختلفة.

    **⭐ النجمة**

    تحصل على نجمة عندما يكون الرقم
    صحيحًا وفي المكان الصحيح.

    **🌙 القمر**

    تحصل على قمر عندما يكون الرقم
    صحيحًا ولكن في المكان الخطأ.

    **❌ لا شيء**

    إذا لم يكن الرقم موجودًا
    في الرمز السري، فلن تحصل على
    نجمة أو قمر مقابل هذا الرقم.

    **👥 عدد اللاعبين**

    يمكن اللعب بشكل فردي أو مع صديق.
    في حالة وجود لاعبين، يتم التناوب
    بينهما بعد كل محاولة.

    **🔟 المحاولات**

    يوجد 10 محاولات مشتركة كحد أقصى.

    **🏆 الفوز**

    يفوز اللاعب عندما يحصل على
    أربع نجوم ⭐⭐⭐⭐.

    **🌧️ الخسارة**

    تنتهي اللعبة إذا استُخدمت
    جميع المحاولات دون اكتشاف الرقم.

    **🔢 ملاحظة**

    الأرقام لا تتكرر، ويمكن أن يبدأ
    الرمز السري بالصفر.
    """)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<p style="
    text-align:center;
    color:#7295ad;
    font-size:12px;
    padding:10px;
">
    ☁️ Stars & Moons 🌙
    <br>
    Made with Python & Streamlit
</p>
""", unsafe_allow_html=True)
