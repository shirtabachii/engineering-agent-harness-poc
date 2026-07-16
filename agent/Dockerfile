FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY langgraph_app/ .

ENTRYPOINT ["python", "graph.py"]
CMD ["/data/sample_cve.json"]
