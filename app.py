from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the 20 Newsgroups dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data
doc_indices = list(range(len(documents)))  # Document numbers for reference

# Create Term-Document Matrix using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(documents)

# Apply LSA using SVD (dimensionality reduction)
lsa = TruncatedSVD(n_components=100)
X_lsa = lsa.fit_transform(X)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data['query']

    # Process the query: Convert to the same LSA space as documents
    query_vec = vectorizer.transform([query])  # Vectorize the user's query
    query_lsa = lsa.transform(query_vec)  # Project the query into the LSA space

    # Compute cosine similarity between the query and documents
    cosine_similarities = cosine_similarity(query_lsa, X_lsa)  # Compare query to documents
    top_indices = np.argsort(cosine_similarities[0])[::-1][:5]  # Get top 5 most similar documents

    # Prepare the top 5 documents and similarity scores
    top_documents = [
        {
            "doc_id": doc_indices[i],  # Document number
            "text": documents[i],  # The document text
            "similarity": cosine_similarities[0][i]  # Cosine similarity score
        }
        for i in top_indices
    ]

    # Return the results as JSON
    return jsonify(documents=top_documents)

if __name__ == '__main__':
    app.run(debug=True)
