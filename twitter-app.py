import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from textblob import TextBlob
import emoji


# Title of the app
# Create two columns, one for the image and one for the title
col1, col2 = st.columns([1, 6])  # 1 for image column, 6 for title column
with col1:

    st.image(r'c:\Users\admin\Downloads\twitter-square-blue-logo-15977.png')
with col2:
    st.title("Twitter Sentiment Analysis")

# Sidebar menu using option_menu
selected = option_menu(None, ['Dashboard', 'Opinion Analysis', 'About'],
                       icons=['house', 'cloud-upload', 'book'], 
                       menu_icon="cast", default_index=0, orientation="horizontal")

# Home page description
if selected == "Dashboard":
    st.write("""
        <h1 style="text-align: center; color: blue;">Welcome to the Twitter Sentiment Analysis App!</h1>
        <p style="color: #FFB6C1;">This app allows you to enter a tweet or any text and predict its sentiment.</p>
        <p style="color: #808080;">The sentiment can be either <strong>Positive</strong> or <strong>Negative</strong>.</p>
    """, unsafe_allow_html=True)
# Sentiment Analysis page
if selected == "Opinion Analysis":
    st.write("### Enter a Tweet or Text for Sentiment Analysis")

    # Text input for tweet
    user_input = st.text_area("Enter the tweet or text:")

    # Load the pre-trained sentiment model and vectorizer
    if st.button("Predict Sentiment"):
        if user_input:
            try:
                # Load pre-trained sentiment analysis model and vectorizer
                with open('tfidf_vectorizer.pkl', 'rb') as f:
                    vectorizer = pickle.load(f)

                # Load the sentiment model
                with open('sentiment_model.pkl', 'rb') as f:
                    sentiment_model = pickle.load(f)

                # Transform user input using the vectorizer
                user_input_transformed = vectorizer.transform([user_input])

                # Predict sentiment (1 for Positive, 0 for Negative)
                sentiment_prediction = sentiment_model.predict(user_input_transformed)

                # Optional: Add TextBlob analysis as a backup or comparison
                textblob_analysis = TextBlob(user_input).sentiment.polarity

                # Display sentiment with emojis
                if textblob_analysis > 0:
                    st.info(f"**Positive** sentiment 😊")
                elif textblob_analysis < 0:
                    st.info(f"**Negative** sentiment 😞")
                else:
                    st.info(f"**Neutral** sentiment 😐")


            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some text to analyze the sentiment.")

# Conclusion page
if selected == "About":
    st.write("""
        # Conclusion
        The sentiment analysis performed on tweets helps in understanding the public's mood or opinion about a given topic, brand, or product.
        
        Some important points:
        - **Positive Sentiment**: Tweets that are optimistic, supportive, or express positive opinions.
        - **Negative Sentiment**: Tweets that are critical, dissatisfied, or express negative opinions.
        
        **Applications**:
        - Social media monitoring for brands.
        - Public opinion analysis for political campaigns.
        - Customer feedback analysis for improving products/services.
        
        Sentiment analysis can be extended by incorporating more complex models or analyzing other emotions such as happiness, sadness, anger, etc. It can also be combined with other data sources to enhance insights.
        
        Thank you for using the Twitter Sentiment Analysis app!
    """)
