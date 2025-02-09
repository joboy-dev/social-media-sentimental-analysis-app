import pandas as pd
import numpy as np
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Load dataset
print('Loading dataset')
df = pd.read_csv('data/csv/tweets.csv')

# Clean data
print('Removing duplicate data')
df.drop_duplicates(inplace=True)

# def clean_text(text: str):
#     text = text.lower()  # Lowercase
#     text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
#     return text

# # Clean text from the dataset
# print('Cleaning text')
# df["sentence"] = df["sentence"].apply(clean_text)

print('Downloading nltk data')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

print('Lemmatizing process begun')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()  # to convert plural to singular or picks the shortest version of a word

def clean_text(text: str):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    tokens = word_tokenize(text)  # Tokenize text
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]  # Lemmatization and stopword removal
    return ' '.join(tokens)

print('Cleaning text')
df["sentence"] = df["sentence"].apply(clean_text)
print(df.tail())

# Model training
print('Train test split')
X_train, X_test, y_train, y_test = train_test_split(df["sentence"], df["sentiment"], test_size=0.35, random_state=42)

# Vectorize text
print('Vectorizing text')
# vectorizer = TfidfVectorizer(max_features=8000)  # Limit features to 5000
vectorizer = TfidfVectorizer(
    max_features=8000,  # Increase feature count
    ngram_range=(1, 2),  # Use unigrams and bigrams
    stop_words='english',  # Remove stopwords
    sublinear_tf=True  # Apply sublinear TF scaling
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the model
print('Training the model')
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)
y_pred = model.predict(X_test_tfidf)

# Get accuracy score
print('Calculating accuracy score')
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
# print('Saving model and vectorizer')
# joblib.dump(model, "models/1-sentiment_model.pkl")
# joblib.dump(vectorizer, "models/1-tfidf_vectorizer.pkl")

print('Training completed successfully!')
