DataNexus: Integrated Analytics Hub

DataNexus is a full-stack automated ETL (Extract, Transform, Load) web application designed to democratize data analytics for non-technical users. It allows business analysts to ingest raw data, perform complex cleaning operations without code, and generate interactive visualizations instantly.

🚀 Live Demo 

https://datanexus.streamlit.app/

📸 Interface Previews

| Ingestion Hub | Visualization Engine |
|  |  |

Figure 1: The Drag-and-Drop Uploader (Left) and Interactive Dashboard (Right).

🌟 Key Features

⚡ High-Performance Ingestion: Implements Lazy Loading and Chunking to handle large datasets (100MB+) without browser crashes.

🧹 Self-Service ETL: A "No-Code" Transformation Hub allows users to:

Drop unnecessary columns.

Handle missing values (Fill with Mean/0 or Drop Rows).

Filter data dynamically.

📈 Interactive Analytics: Powered by Plotly, users can zoom, pan, and drill down into data points.

💾 Smart Architecture: Utilizes Session State caching to ensure data persistence across user interactions.

🛠️ Tech Stack

Frontend: Streamlit (Web Framework)

Backend: Python, Pandas (Data Processing)

Visualization: Plotly Express

Performance: NumPy (Vectorization)

💻 Installation (Run Locally)

Clone the repository:

git clone [https://github.com/Speardrex/DataNexus_webapp.git](https://github.com/Speardrex/DataNexus_webapp.git)
cd DataNexus



Install dependencies:

pip install -r requirements.txt



Run the app:

streamlit run app.py



🔄 How It Works (ETL Pipeline)

Extract: User uploads a raw .csv or .xlsx file.

Transform: The Pandas engine cleans the data in-memory based on user widget inputs.

Load: The cleaned data is visualized on the dashboard and available for export/download.

👨‍💻 Author

Speardrex
