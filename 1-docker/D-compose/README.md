# Minimal Docker Compose Example (Frontend + Backend)
 This project demonstrates a minimal docker-compose setup with two services,both running Python:
 - frontend: A simple Streamlit server for the web UI.
 - backend: A Python FastAPI server that receives data and saves it to disk.

 # Project Structure
 ```
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```


- `docker compose build`
- `docker compose up`
- `docker compose down`
