from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample training data
emails = [
    "Win money now",
    "Limited offer just for you",
    "Hello friend how are you",
    "Meeting tomorrow",
    "Congratulations you won prize",
    "Let's study together"
]

labels = [1, 1, 0, 0, 1, 0]
# 1 = Spam, 0 = Not Spam

# Convert text to numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

# Train model
model = MultinomialNB()
model.fit(X, labels)


def check_email(text):
    text_vec = vectorizer.transform([text])
    result = model.predict(text_vec)

    if result[0] == 1:
        return "Spam"
    else:
        return "Not Spam"


# Test
print(check_email("Win prize now"))