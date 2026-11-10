FROM python:3.11-slim

LABEL maintainer="equipe-ia"
LABEL description="Service IA de depistage de la retinopathie diabetique"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV EYE_CHECKER_MODEL_PATH=models/eye_checker.pt
ENV STAGE_CLASSIFIER_MODEL_PATH=models/stage_classifier.pt

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY core/ ./core/
COPY models/ ./models/

EXPOSE 8001

CMD ["python", "app.py"]
