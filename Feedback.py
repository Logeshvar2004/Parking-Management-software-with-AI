import streamlit as st
import pandas as pd
from datetime import datetime
from textblob import TextBlob

# Function to check authentication
def authenticate(username):
    return username == "parkit-admin"

# Function to analyze sentiment
def analyze_sentiment(feedback):
    analysis = TextBlob(feedback)
    sentiment_score = analysis.sentiment.polarity
    return sentiment_score

def collect_user_feedback():
    st.subheader("Collect User Feedback")

    # Get user feedback
    user_feedback = st.text_area("Provide your feedback:")

    # Additional information you may want to collect, such as user ID or timestamp
    user_id = st.text_input("User ID (optional):")  # You can skip this or use a login system
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Submit Feedback"):
        feedback_data = {
            'timestamp': [timestamp],
            'user_id': [user_id],
            'feedback': [user_feedback]
        }

        feedback_df = pd.DataFrame(feedback_data)

        # Save the feedback to a CSV file (you can use a database in a real application)
        try:
            existing_data = pd.read_csv('user_feedback.csv')
            updated_data = pd.concat([existing_data, feedback_df], ignore_index=True)
            updated_data.to_csv('user_feedback.csv', index=False)
        except FileNotFoundError:
            feedback_df.to_csv('user_feedback.csv', index=False)

        st.success("Thank you for your feedback!")

def classify_sentiment(sentiment_score):
    # Classify sentiment into categories
    if sentiment_score < 0:
        return "Negative"
    elif sentiment_score == 0:
        return "Neutral"
    else:
        return "Positive"

def analyze_entire_dataset(feedback_data):
    st.subheader("Sentiment Analysis Results")

    # Analyze sentiment for each feedback entry
    feedback_data['Sentiment'] = feedback_data['feedback'].apply(lambda x: classify_sentiment(analyze_sentiment(x)))

    # Calculate percentages
    total_entries = len(feedback_data)
    positive_percentage = (feedback_data['Sentiment'] == 'Positive').sum() / total_entries * 100
    negative_percentage = (feedback_data['Sentiment'] == 'Negative').sum() / total_entries * 100
    neutral_percentage = (feedback_data['Sentiment'] == 'Neutral').sum() / total_entries * 100

    st.write(f"Overall Sentiment Category for the Entire Dataset:")
    st.write(f"- Positive: {positive_percentage:.2f}%")
    st.write(f"- Negative: {negative_percentage:.2f}%")
    st.write(f"- Neutral: {neutral_percentage:.2f}%")

def display_recent_feedback():
    st.subheader("Recent Feedback")

    # Display the 10 most recent feedback entries
    try:
        feedback_data = pd.read_csv('user_feedback.csv')
        recent_feedback = feedback_data.tail(10)
        st.dataframe(recent_feedback)
    except FileNotFoundError:
        st.info("No feedback available yet.")

# Main Streamlit app
def main():
    st.title("User Feedback App")

    # Collect user feedback
    collect_user_feedback()
    st.subheader('\n')
    st.subheader('Give the authentication code to get the sentiment analysis')    
    us= st.text_input('', type='password')
    if st.button("Analyze"):

        if authenticate(us):
            # Display recent feedback and perform sentiment analysis
            display_recent_feedback()
            analyze_entire_dataset(pd.read_csv('user_feedback.csv'))
        else:
            st.warning("Authentication failed. Please check your username.")

if __name__ == "__main__":
    main()
