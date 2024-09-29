from flask import Flask, render_template, jsonify, request
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

# Global variable to store the dataset
data = None

@app.route('/generate_data', methods=['GET'])
def generate_data():
    global data  # Access the global variable
    # Generates random 2D data for clustering
    data, _ = make_blobs(n_samples=300, centers=4, n_features=2, cluster_std=3, random_state=None)
    return jsonify(data.tolist())

@app.route('/kmeans', methods=['POST'])
def kmeans():
    try:
        # Expecting a JSON request body with data and number of clusters (k)
        content = request.json
        data = np.array(content['data'])
        k = content['k']

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=k, init='random', random_state=42)
        kmeans.fit(data)

        centroids = kmeans.cluster_centers_.tolist()
        labels = kmeans.labels_.tolist()

        return jsonify({'centroids': centroids, 'labels': labels})

    except Exception as e:
        # Catch any error and return it as a response
        return jsonify({'error': str(e)}), 400

# Initialization Methods: Random
@app.route('/initialize_random', methods=['POST'])
def initialize_random():
    global data  # Access the global dataset
    k = int(request.json.get('k'))  # Get the number of clusters from the request
    
    # Check if data has been generated
    if data is None:
        return jsonify({"error": "No dataset generated yet. Please generate data first."}), 400
    
    # Call the random initialization function
    centroids = initialize_random_centroids(data, k)
    return jsonify(centroids.tolist())

def initialize_random_centroids(data, k):
    """
    Randomly initialize centroids by selecting k random points from the data.
    """
    indices = np.random.choice(data.shape[0], size=k, replace=False)  # Randomly choose k unique points
    centroids = data[indices]
    return centroids


# Initialization Methods: Farthest First
@app.route('/initialize_farthest', methods=['POST'])
def initialize_farthest():
    global data  # Access the global dataset
    k = int(request.json.get('k'))  # Get the number of clusters from the request
    
    # Check if data has been generated
    if data is None:
        return jsonify({"error": "No dataset generated yet. Please generate data first."}), 400
    
    # Call the Farthest First initialization function
    centroids = initialize_farthest_centroids(data, k)
    return jsonify(centroids.tolist())

def initialize_farthest_centroids(data, k):
    """
    Initialize centroids using the Farthest First approach.
    
    Parameters:
    - data: The dataset (array of points).
    - k: The number of centroids to initialize.

    Returns:
    - centroids: Array of k centroids chosen to be farthest apart.
    """
    # Randomly select the first centroid
    centroids = [data[np.random.randint(0, data.shape[0])]]

    # Select remaining centroids
    for _ in range(1, k):
        # Calculate the distance between each point and the nearest centroid
        distances = np.array([min(np.linalg.norm(point - centroid) for centroid in centroids) for point in data])

        # Choose the point that is farthest from any centroid
        farthest_point = data[np.argmax(distances)]
        centroids.append(farthest_point)

    return np.array(centroids)

# Initialization Methods: KMeans++
@app.route('/initialize_kmeans_plus_plus', methods=['POST'])
def initialize_kmeans_plus_plus():
    global data  # Access the global dataset
    k = int(request.json.get('k'))  # Get the number of clusters from the request
    
    # Check if data has been generated
    if data is None:
        return jsonify({"error": "No dataset generated yet. Please generate data first."}), 400
    
    # Call the KMeans++ initialization function
    centroids = initialize_kmeans_plus_plus(data, k)
    return jsonify(centroids.tolist())

def initialize_kmeans_plus_plus(data, k):
    """
    Initialize centroids using the KMeans++ method.
    
    Parameters:
    - data: The dataset (array of points).
    - k: The number of centroids to initialize.

    Returns:
    - centroids: Array of k centroids initialized using KMeans++.
    """
    # Randomly select the first centroid
    centroids = [data[np.random.randint(0, data.shape[0])]]

    # Select the remaining k-1 centroids
    for _ in range(1, k):
        # Calculate the distance from each point to the nearest centroid
        distances = np.array([min(np.linalg.norm(point - centroid)**2 for centroid in centroids) for point in data])

        # Probabilistically select the next centroid
        probabilities = distances / np.sum(distances)
        cumulative_probabilities = np.cumsum(probabilities)
        r = np.random.rand()

        # Select the data point corresponding to r
        next_centroid_index = np.where(cumulative_probabilities >= r)[0][0]
        centroids.append(data[next_centroid_index])

    return np.array(centroids)

# Initialization Methods: Manuel
@app.route('/store_manual_centroids', methods=['POST'])
def store_manual_centroids():
    global manual_centroids  # Store the manually selected centroids globally
    manual_centroids = request.json.get('centroids')  # Get the centroids from the request
    return jsonify({"status": "Centroids stored successfully."})

if __name__ == "__main__":
    app.run(debug=True)
