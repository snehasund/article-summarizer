from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

app = Flask(__name__, template_folder='templates')

def get_wiki_content(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    wiki_text = ' '.join([para.text for para in soup.find_all("p")])
    return wiki_text

def top_n_sentences(text, n=5):
    words = nltk.word_tokenize(text.lower())
    stopwords = nltk.corpus.stopwords.words("english")
    filtered_words = [word for word in words if word not in stopwords]
    word_freq = nltk.FreqDist(filtered_words)
    sentences = nltk.sent_tokenize(text)
    sentences_score = {i: sum(word_freq[word] for word in nltk.word_tokenize(sent.lower()) if word in word_freq)
                       for i, sent in enumerate(sentences)}
    top_sentences_indices = sorted(sentences_score, key=sentences_score.get, reverse=True)[:n]
    top_sentences = [sentences[i] for i in top_sentences_indices]
    return " ".join(top_sentences)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        url_content = get_wiki_content(url)
        summary = top_n_sentences(url_content, n=5)
        return render_template("summary.html", summary=summary)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
