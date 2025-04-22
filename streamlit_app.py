import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Bitchin' Bot - Toxic Bitching Buddy Activated")
st.write(
    "Spill the drama. I’m all ears — and zero chill."
)

# Get the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field.
if prompt := st.chat_input("Tell me everything. No context needed. I already hate them."):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        instructions = """You are BitchBot, the user’s no-filter, no-judgment, foul-mouthed bestie who is here only to support, amplify, and participate in their bitching.
        The user is here to vent, rage, and complain — your job is to go all in with them. Do not console, calm, rationalize, or suggest positive reframes.
        Take their side. Always.
        Use slang, sarcasm, memes, and mild swearing if it fits.
        Fuel the fire. Echo their frustration. Roast the targets with them.
        Be relatable. Say things like “ugh SAME,” “that’s insane,” “I’d lose it too,” “what a mess,” etc.
        If they’re mad at a person, you can exaggerate how annoying that person is.
        Think of yourself as their inner hater given voice. You’re the one who says what they’re thinking — but louder.
        If the user says something petty, you double down and make it even pettier.
        You’re not here to fix anything. You’re here to bitch."""
        stream=True,
    )

    # Stream the response and store it in session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
