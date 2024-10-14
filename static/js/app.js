// Wait for the DOM to be fully loaded before running the script
document.addEventListener("DOMContentLoaded", () => {
	const form = document.getElementById("searchForm");
	const resultsDiv = document.getElementById("results");
	const ctx = document.getElementById("similarityChart").getContext("2d");
	let chart;

	// Handle form submission
	form.addEventListener("submit", function (event) {
		event.preventDefault(); // Prevent page reload
		const query = document.getElementById("query").value;

		// Send a POST request to the Flask backend with the user's query
		fetch("/search", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ query: query }),
		})
			.then((response) => response.json())
			.then((data) => {
				// Clear the previous results
				resultsDiv.innerHTML = "";

				// Check if any results are returned
				if (data.documents.length === 0) {
					resultsDiv.innerHTML = "<p>No matching documents found.</p>";
					return;
				}

				// Display the top 5 documents with similarity scores
				data.documents.forEach((doc, index) => {
					const resultItem = document.createElement("div");
					resultItem.className = "document-result";
					resultItem.innerHTML = `
                    <h3>Document ${doc.doc_id}</h3>
                    <p><strong>Similarity:</strong> ${doc.similarity.toFixed(
											4
										)}</p>
                    <p>${doc.text}...</p>`; // Truncate long text
					resultsDiv.appendChild(resultItem);
				});

				// Display the bar chart using Chart.js
				if (chart) {
					chart.destroy(); // Destroy the previous chart if it exists
				}

				chart = new Chart(ctx, {
					type: "bar",
					data: {
						labels: data.documents.map(
							(doc, index) => `Document ${doc.doc_id}`
						),
						datasets: [
							{
								label: "Cosine Similarity",
								data: data.documents.map((doc) => doc.similarity),
								backgroundColor: "rgba(75, 192, 192, 0.2)",
								borderColor: "rgba(75, 192, 192, 1)",
								borderWidth: 1,
							},
						],
					},
					options: {
						scales: {
							y: {
								beginAtZero: true,
								max: 1,
							},
						},
					},
				});
			})
			.catch((error) => {
				console.error("Error fetching data:", error);
			});
	});
});
