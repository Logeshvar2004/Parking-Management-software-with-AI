import sys
sys.path.append('D:\Coding\python\KPR-Hackathon')

import streamlit as st
import numpy as np
import pandas as pd
import shelve
from datetime import datetime
import random
from textblob import TextBlob
from Space.streamlit2 import calc_diff, main as space_main
from chatbot.streamlit import (
    clean_up_sentence,
    bag_of_words,
    predict_class,
    get_response,
    load_chat_history,
    save_chat_history,
    main as chatbot_main
)
from Feedback.main import (
    authenticate,
    analyze_sentiment,
    collect_user_feedback,
    classify_sentiment,
    analyze_entire_dataset,
    display_recent_feedback,
    main as feedback_main
)
from Location.streamlit import(
    get_user_location,
    find_nearby_places,
    main as Search_Location
)

def main():
    st.title("Parkit")

    selected_option = st.sidebar.selectbox("Select App", ["Space App", "Chatbot App", "Feedback App", "Nearby parkings"])

    if selected_option == "Space App":
        space_app()
    elif selected_option == "Chatbot App":
        chatbot_app()
    elif selected_option == "Feedback App":
        feedback_app()
    elif selected_option == "Nearby parkings":
        Location_app()

def space_app():
    space_main()

def chatbot_app():
    chatbot_main()

def feedback_app():
    feedback_main()

def Location_app():
    Search_Location()

if __name__ == "__main__":
    main()