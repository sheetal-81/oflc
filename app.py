from flask import Flask, render_template, request
import pickle  # Import pickle
from sklearn.feature_extraction.text import CountVectorizer

# Load your vectorizer (this should be the same one you used when training your model)
vectorizer = pickle.load(open('trash/spam_mail_vectorizer.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/OurTeam')
def our_team():
    return render_template('OurTeam.html')

@app.route('/Notification')
def notification():
    return render_template('Notification.html')

@app.route('/Login')
def login():
    return render_template('Login.html')

@app.route('/search_url', methods=['POST'])
def search_url():
    query = request.form['query']
    # Load your model for URL checking
    url_model = pickle.load(open('trash/phishing.pkl', 'rb'))
    # Predict the result
    result = url_model.predict([query])
    # Return the result
    return '<h1>The URL is ' + ('Safe' if result[0] == 'good' else 'Unsafe') + '</h1>'

@app.route('/search_email', methods=['POST'])
def search_email():
    email_content = request.form['email']
    # Transform your email content into a numerical form
    email_content_transformed = vectorizer.transform([email_content])
    # Load your model for email checking
    email_model = pickle.load(open('trash/spam_mail_model.pkl', 'rb'))
    # Predict the result
    result = email_model.predict(email_content_transformed)  # Use 'email_content_transformed' instead of '[[email_content]]'
    # Return the result
    return '<h1>The email is ' + ('Safe' if result[0] == 'good' else 'Unsafe') + '</h1>'


if __name__ == "__main__":
    app.run(debug=True, port=5001)
