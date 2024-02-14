import streamlit as st
import random
import json
import pickle
import numpy as np
import nltk
import shelve
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('D:\Coding\python\KPR-Hackathon\chatbot\intents.json').read())
words = pickle.load(open('D:\Coding\python\KPR-Hackathon\chatbot\words.pkl', 'rb'))
classes = pickle.load(open('D:\Coding\python\KPR-Hackathon\chatbot\classes.pkl', 'rb'))
model = load_model('D:\Coding\python\KPR-Hackathon\chatbot\chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

def main():
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()

    header = st.container()
    header.title("Parkit")
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            background-color: white;
            z-index: 999;
        }
    </style>
        """,
        unsafe_allow_html=True
    )
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_response(predict_class(prompt), intents)
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    save_chat_history(st.session_state.messages)

if __name__ == "__main__":
    main()