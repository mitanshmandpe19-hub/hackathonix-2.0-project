from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import tkinter as tk

# Training data
emails = [
    "Win money now",
    "Limited offer just for you",
    "Hello friend how are you",
    "Meeting tomorrow",
    "Congratulations you won prize",
    "Let's study together"
]

labels = [1, 1, 0, 0, 1, 0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

model = MultinomialNB()
model.fit(X, labels)


def check_email():
    text = entry.get()
    text_vec = vectorizer.transform([text])

    result = model.predict(text_vec)
    probability = model.predict_proba(text_vec)

    spam_prob = probability[0][1] * 100

    if result[0] == 1:
        output_label.config(text=f"Spam {spam_prob:.2f}%")
    else:
        output_label.config(text=f"Not Spam {100-spam_prob:.2f}%")


# GUI --------
def clear_text():
    entry.delete(0, tk.END)
    output_label.config(text="")

window = tk.Tk()
window.title("Spam Email Detector")
window.geometry("500x300")
window.configure(bg="#f0f0f0")


title = tk.Label(
    window,
    text="Spam Email Detector",
    font=("Arial", 18, "bold"),
    bg="#f0f0f0"
)
title.pack(pady=10)


label = tk.Label(
    window,
    text="Enter Email Text:",
    font=("Arial", 12),
    bg="#f0f0f0"
)
label.pack()


entry = tk.Entry(
    window,
    width=45,
    font=("Arial", 12)
)
entry.pack(pady=5)


button = tk.Button(
    window,
    text="Check",
    font=("Arial", 12),
    bg="blue",
    fg="white",
    command=check_email
)
button.pack(pady=5)


clear_btn = tk.Button(
    window,
    text="Clear",
    font=("Arial", 12),
    bg="red",
    fg="white",
    command="clear_text"
)
clear_btn.pack(pady=5)


output_label = tk.Label(
    window,
    text="",
    font=("Arial", 14),
    bg="#f0f0f0"
)
output_label.pack(pady=10)


window.mainloop()