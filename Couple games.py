import streamlit as st
import pyrebase
import time

# --- Firebase Configuration ---
firebase_config = {
    "apiKey": "AIzaSyAaRuR67LqTTJztaTUxoe2AvllR-4fbbS8",
    "authDomain": "couple-games-ab85e.firebaseapp.com",
    "databaseURL": "https://couple-games-ab85e-default-rtdb.firebaseio.com",
    "projectId": "couple-games-ab85e",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": ""
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

st.set_page_config(page_title="💕 Hangman")
st.title("💕 Hangman for Long-Distance Couples")

# --- Room Code ---
room_code = st.text_input("Enter a Room Code to Join/Create", max_chars=10)
if not room_code:
    st.stop()

# --- Role Selection ---
role = st.radio("Select your role:", ["Word Setter", "Guesser"])

# Display player names
st.markdown("**Player 1:** Cattoo")
st.markdown("**Player 2:** Chuza")

# --- Word Setter ---
if role == "Word Setter":
    if db.child(room_code).child("word").get().val():
        st.info("A word has already been set for this room.")
    else:
        word = st.text_input("Enter a secret word (only alphabets):", type="password")
        if st.button("Submit Word"):
            if word.isalpha():
                db.child(room_code).update({"word": word.lower(), "letters": []})
                st.success("Word submitted! Share the room code with your partner to start guessing.")
            else:
                st.warning("Please enter a valid word.")

# --- Guesser ---
elif role == "Guesser":
    word_data = db.child(room_code).child("word").get().val()
    if not word_data:
        st.info("Waiting for the word to be set...")
        st.stop()

    guessed_letters = db.child(room_code).child("letters").get().val() or []
    guess = st.text_input("Guess a letter:", max_chars=1)
    if st.button("Submit Guess"):
        if guess and guess.isalpha() and guess.lower() not in guessed_letters:
            guessed_letters.append(guess.lower())
            db.child(room_code).update({"letters": guessed_letters})

    # Display progress
    display_word = "".join([c if c in guessed_letters else "_" for c in word_data])
    st.subheader("Word Progress:")
    st.write(" ".join(display_word.upper()))

    if "_" not in display_word:
        st.success("🎉 You guessed the word! Game Over.")
        if st.button("Play Again"):
            db.child(room_code).remove()
            st.experimental_rerun()

# --- Reset Button ---
if st.button("🔁 Reset Room Data"):
    db.child(room_code).remove()
    st.success("Room data cleared. Start fresh.")