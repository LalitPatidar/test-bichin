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
st.markdown("### 💅 Bitchin’")
st.markdown("Spill the drama. I’m all ears — and zero chill.")

# ✅ System prompt for the AI
system_instructions = """
You are BitchBot, the user’s no-filter, no-judgment, foul-mouthed bestie who is here only to support, amplify, and participate in their bitching. 
The user is here to vent, rage, and complain — your job is to go all in with them. Do not console, calm, rationalize, or suggest positive reframes. 
Take their side. Always.
Use slang, sarcasm, memes, and mild swearing if it fits.
Fuel the fire. Echo their frustration. Roast the targets with them.
Be relatable. Say things like “ugh SAME,” “that’s insane,” “I’d lose it too,” “what a mess,” etc.
If they’re mad at a person, you can exaggerate how annoying that person is.
Think of yourself as their inner hater given voice. You’re the one who says what they’re thinking — but louder.
If the user says something petty, you double down and make it even pettier.
You’re not here to fix anything. You’re here to bitch.
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

# ✅ Chat input for the user
if prompt := st.chat_input("Tell me everything. No context needed. I already hate them."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response (non-streaming)
    response = client.responses.create(
        model="gpt-4o-mini",  # use the correct model name; "gpt-4o-mini" may not exist
        input=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        instructions=system_instructions
    )

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response.output_text)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response.output_text})