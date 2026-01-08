DataNexus: Integrated Analytics Hub

DataNexus is a full-stack automated ETL (Extract, Transform, Load) web application designed to democratize data analytics for non-technical users. It allows business analysts to ingest raw data, perform complex cleaning operations without code, and generate interactive visualizations instantly.

🚀 Live Demo 

https://datanexus.streamlit.app/


## 🏗️ System Architecture

The application follows a modular **ETL (Extract, Transform, Load)** architecture powered by Streamlit's reactive framework.

![System Architecture](https://github.com/Speardrex/DataNexus_webapp/blob/main/asset/DataNexusHub-2026-01-07-073514.png)

Key Architectural Decisions:
* **Lazy Loading:** Implemented via `@st.cache_data` to optimize memory usage for large datasets (O(n) complexity).
* **State Management:** Utilizes `st.session_state` to persist data across user interactions (filtering, cleaning) in a stateless web environment.
* **In-Memory Processing:** Ensures data privacy by processing files in RAM without permanent server storage.


**Interface Previews**

| Ingestion Hub |

![Ingestion Hub](https://github.com/Speardrex/DataNexus_webapp/blob/main/asset/Ingestion.png)


⚡ Key Features:

  - The Drag-and-Drop Uploader (Left) and Interactive Dashboard (Right).
  - High-Performance Ingestion: Implements Lazy Loading and Chunking to handle large datasets (100MB+) without browser crashes.

| ETL Process |

![ETL Hub](https://github.com/Speardrex/DataNexus_webapp/blob/main/asset/ETL.png)

🧹 Self-Service ETL: A "No-Code" Transformation Hub allows users to:

 -  Drop unnecessary columns.
 -  Handle missing values (Fill with Mean/0 or Drop Rows).
 -  Filter data dynamically.

| Visualization Engine |

![Vis Hub](https://github.com/Speardrex/DataNexus_webapp/blob/main/asset/visualtisation.png)

📈 Interactive Analytics: 

 -  Powered by Plotly, users can zoom, pan, and drill down into data points.

💾 Smart Architecture: Utilizes Session State caching to ensure data persistence across user interactions.

Tech Stack:

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
