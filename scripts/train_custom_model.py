import pandas as pd
import numpy as np
import re
import joblib
import emoji
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report,  precision_score, recall_score, f1_score
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.svm import SVC


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
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

print('Lemmatizing process begun')
english_stopwords = stopwords.words('english')
other_stopwords = [
    "na", "onye", "gi", "ka", "ya", "m", "ndi", "a", "o", "nke",
    "di", "ihe", "i", "no", "bu", "anyi", "ga", "igbo", "gị", "ike",
    "chukwu", "ọ", "biko", "e", "ma", "nwanne", "oma", "aka", "mma", "nna",
    "nwa", "ndị", "ha", "egwu", "the", "unu", "kwa", "ebe", "nne", "eme",
    "isi", "bụ", "dị", "maka", "nwoke", "si", "anyị", "okwu", "ji", "ego",
    "obi", "anya", "otu", "mgbe", "oge", "ị", "onwe", "ala", "mana", "eji",
    "da", "allah", "ya", "a", "ba", "ta", "na", "wannan", "ne", "kuma",
    "su", "sai", "mu", "yan", "ko", "mai", "dai", "shi", "ka", "yayi",
    "to", "amma", "ga", "haka", "yi", "daga", "ma", "duk", "kai", "masu",
    "wani", "sun", "zai", "sa", "ina", "nan", "idan", "wanda", "an", "ce",
    "ke", "suka", "cikin", "wa", "daya", "kasa", "iya", "yake", "domin",
    "in", "kan", "yana", "aka", "za", "me", "don", "har", "ake", "gaba",
    "akwai", "yadda", "abin", "di", "abeg", "wetin", "sef", "abi", "wahala",
    "comot", "shey", "pikin", "pesin", "sey", "deh", "weda", "pipo", "kon",
    "tok", "dis", "im", "bin", "wit", "fit", "de", "oda", "don", "e",
    "dat", "wen", "d", "kain", "tins", "na", "wia", "dey", "tó", "àwọn",
    "ń", "pé", "tí", "ṣe", "máa", "ní", "wọ́n", "ó", "ni", "kí",
    "sì", "sí", "jẹ́", "ti", "bá", "a", "fi", "lè", "náà", "kan",
    "fún", "láti", "rẹ̀", "sọ", "wọn", "ohun", "àti", "bí", "nínú", "wà",
    "kò", "wa", "wá", "yìí", "ló", "rí", "kó", "ká", "lọ", "o",
    "mi", "mo", "gbogbo", "ọmọ", "ò", "í", "ẹ", "á", "ọ̀rọ̀", "ẹni",
    "ara", "fẹ́", "i", "wo", "gbé", "pa", "ọdún", "di", "kì", "yóò"
]
stopwords = set(english_stopwords + other_stopwords)
print(stopwords)
lemmatizer = WordNetLemmatizer()  # to convert plural to singular or picks the shortest version of a word

def clean_text(text: str):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"#\w+", "", text)  # Remove hashtags
    text = re.sub(r"@\w+", "", text)  # Remove mentions
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    text = emoji.replace_emoji(text, replace="")  # Remove emojis
    tokens = word_tokenize(text)  # Tokenize text
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stopwords]  # Lemmatization and stopword removal
    return ' '.join(tokens)


print('Cleaning text')
df["sentence"] = df["sentence"].apply(clean_text)
print(df.tail())

# Model training
print('Train test split')
X_train, X_test, y_train, y_test = train_test_split(df["sentence"], df["sentiment"], test_size=0.35, random_state=42)

# Vectorize text
print('Vectorizing text')
vectorizer = TfidfVectorizer(max_features=8000)  # Limit features to 5000
# vectorizer = TfidfVectorizer(
#     max_features=8000,  # Increase feature count
#     ngram_range=(1, 2),  # Use unigrams and bigrams
#     stop_words='english',  # Remove stopwords
#     sublinear_tf=True  # Apply sublinear TF scaling
# )
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the model
print('Training the model')
model = LogisticRegression()
# model = SVC(kernel="linear")  # Using linear kernel for text data
model.fit(X_train_tfidf, y_train)
y_pred = model.predict(X_test_tfidf)

# Calculate evaluation metrics
print('Calculating metrics')
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

# Print results
print(f"Model Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Classification report (still useful for a breakdown)
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
print('Saving model and vectorizer')
joblib.dump(model, "models/2-sentiment_model.pkl")
joblib.dump(vectorizer, "models/2-tfidf_vectorizer.pkl")

print('Training completed successfully!')
