FROM python:3.11-slim

WORKDIR /app

COPY src/app/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY src/app /app
COPY src/vector_twin /app/vector_twin

EXPOSE 8501

CMD ["streamlit", "run", "main.py"] 
