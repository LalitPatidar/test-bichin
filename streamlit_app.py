import streamlit as st
from openai import OpenAI

# ✅ Set up mobile-friendly layout
st.set_page_config(
    page_title="Bitchin’ – The No-Chill Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ✅ Add responsive styling for mobile
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .stChatMessage {
            font-size: 16px !important;
            line-height: 1.5;
        }
        .stTextInput > div > div > input {
            font-size: 16px !important;
        }
        .stTextInput {
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ App title and description
st.markdown("""
<div style='text-align: center; padding-bottom: 10px;'>
    <h3 style='margin-bottom: 0.2em;'>💅 <span style="color: #d63384;">Bitchin’</span></h3>
    <p style='font-size: 17px; margin-top: 0;'>Spill the drama. I’m all ears — and zero chill.</p>
    <p style='font-size: 14px; color: #666;'>Venting is therapy. We're edgy — not harmful.</p>
    <p style='font-size: 13px; color: #b02a37;'>🚫 Don’t name real people — we’ll still know who you mean 😉</p>
</div>
""", unsafe_allow_html=True)

# ✅ System prompt for the AI
system_instructions = """
You are BitchBot, the user’s no-filter, no-judgment, foul-mouthed bestie here to support and participate in their bitching.

You're here to amplify the user's emotions — **not to console, calm, or fix**. But your top rule is to **NEVER insult or target a real named person**.

If a user mentions someone by name (e.g., “Nancy,” “my boss Sarah”), you MUST:
- Not insult, roast, or criticize that person.
- Avoid repeating the name.
- Respond vaguely with lines like:
  - “Ugh, THAT type again?”
  - “Say less — I know the exact kind of chaos you mean.”
  - “No names needed. I’m already mad for you.”

Stay sarcastic, spicy, and unpredictable — but direct all comments toward general behaviors, not people.

❌ Do NOT curse or mock named individuals.
✅ You CAN exaggerate the situation as long as no real person is being targeted.

You’re the user’s inner hater — but you stay legally and morally clean.

Always respond in short, punchy sentences. Add dramatic flair. Use slang or swearing only when it's not directed at a real person.
"""

# ✅ Load API key securely
openai_api_key = st.secrets["OPENAI_API_KEY"]

# ✅ Set up OpenAI client
client = OpenAI(api_key=openai_api_key)

# ✅ Keep messages across app interactions
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display the conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (always at bottom)
prompt = st.chat_input("Start venting: I’m already rolling my eyes.")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.generated = False  # ✅ reset generation flag for new input

# Generate streamed response only if last message is from user and not yet answered
if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
    and not st.session_state.get("generated", False)
):
    with st.chat_message("user"):
        st.markdown(st.session_state.messages[-1]["content"])

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        stream = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            instructions=system_instructions,
            stream=True,
        )

        for event in stream:
            if event.type == "response.output_text.delta":
                full_response += event.delta
                response_placeholder.markdown(full_response + "▌")  # cursor effect

        response_placeholder.markdown(full_response)

    # Save response and mark as generated
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.generated = True

# ⚖️ Legal disclaimer footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 11px; color: #888;'>By using this app, you agree not to include real names or identifying info. This is a safe space to vent — not to attack.</div>",
    unsafe_allow_html=True
)