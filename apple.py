from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import tkinter as tk
import re

# Training data
emails = [
    "Win money now",
    "Limited offer just for you",
    "Hello friend how are you",
    "Meeting tomorrow",
    "Congratulations you won prize",
    "Let's study together",
    "Congratulations! You have won iPhone",
    "Urgent! Your account will be suspended",
    "See you at the event tonight",
    "thank you for your help",
    "Your KYC is pending. Verify now to continue services",
    "i will call you later",
    "Congratulations! Your PAN card has been selected for an exclusive banking reward- click here to claim now",
    "Urgent: Verify your Aadhaar details immediately to avoid suspension of your bank account",
    "Dear customer, your bank account has unusual activity; provide your PAN and Aadhaar details to secure it",
    "I applied for my pan card last week",
    "The bank sends sms for every transaction",
    "I checked my bank balance today"
]

labels = [1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

model = MultinomialNB()
model.fit(X, labels)

# Fraud keyword categories
kyc_words = ["kyc", "verify", "aadhaar", "pan"]
lottery_words = ["lottery", "winner", "won", "prize", "congratulations"]
offer_words = ["offer", "free", "gift", "discount", "deal"]
investment_words = ["investment", "profit", "crypto"]

def detect_category(text):
    text = text.lower()
    if any(word in text for word in kyc_words):
        return "🏦 KYC Scam"
    elif any(word in text for word in lottery_words):
        return "🎉 Lottery Scam"
    elif any(word in text for word in offer_words):
        return "🎁 Fake Offer"
    elif any(word in text for word in investment_words):
        return "💰 Investment Scam"
    else:
        return "Unknown"

# Analyze sender email
def check_sender(email):
    trusted_domains = ["gmail.com", "outlook.com", "yahoo.com"]
    domain = email.split("@")[-1]
    if domain in trusted_domains:
        return "Trusted Email Provider"
    else:
        return "⚠ Suspicious Domain"

# Extract IP from email header
def extract_ip(header):
    ip = re.search(r"\d+\.\d+\.\d+\.\d+", header)
    if ip:
        return ip.group()
    else:
        return "IP Not Found"

def check_email():
    text = entry.get()
    sender = sender_entry.get()
    header = header_entry.get("1.0", tk.END)  # Multi-line input for headers

    text_vec = vectorizer.transform([text])
    result = model.predict(text_vec)
    probability = model.predict_proba(text_vec)
    spam_prob = probability[0][1] * 100

    category = detect_category(text)
    sender_status = check_sender(sender)
    sender_ip = extract_ip(header)

    if result[0] == 1:
        output_label.config(
            text=f"🚫 Spam {spam_prob:.2f}%\nType: {category}\nSender Status: {sender_status}\nSender IP: {sender_ip}",
            fg="red"
        )
    else:
        output_label.config(
            text=f"✅ Not Spam {100-spam_prob:.2f}%\nSender Status: {sender_status}\nSender IP: {sender_ip}",
            fg="green"
        )

# GUI
def clear_text():
    entry.delete(0, tk.END)
    sender_entry.delete(0, tk.END)
    header_entry.delete("1.0", tk.END)
    output_label.config(text="")

window = tk.Tk()
window.title("Spam Email Detector")
window.geometry("600x500")
window.configure(bg="#f0f0f0")

title = tk.Label(window, text="Spam Email Detector", font=("Arial", 18, "bold"), bg="#f0f0f0")
title.pack(pady=10)

sender_label = tk.Label(window, text="Sender Email:", font=("Arial", 12), bg="#f0f0f0")
sender_label.pack()
sender_entry = tk.Entry(window, width=50, font=("Arial", 12))
sender_entry.pack(pady=5)

label = tk.Label(window, text="Enter Email Text:", font=("Arial", 12), bg="#f0f0f0")
label.pack()
entry = tk.Entry(window, width=50, font=("Arial", 12))
entry.pack(pady=5)

header_label = tk.Label(window, text="Paste Email Header (for IP detection):", font=("Arial", 12), bg="#f0f0f0")
header_label.pack()
header_entry = tk.Text(window, width=70, height=5, font=("Arial", 10))
header_entry.pack(pady=5)

button = tk.Button(window, text="Check", font=("Arial", 12), bg="blue", fg="white", command=check_email)
button.pack(pady=5)

clear_btn = tk.Button(window, text="Clear", font=("Arial", 12), bg="red", fg="white", command=clear_text)
clear_btn.pack(pady=5)

output_label = tk.Label(window, text="", font=("Arial", 14), bg="#f0f0f0")
output_label.pack(pady=10)

window.mainloop()