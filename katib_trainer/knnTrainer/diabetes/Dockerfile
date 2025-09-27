FROM python:3.11-slim

WORKDIR /opt
RUN mkdir knn
RUN mkdir knn/models

COPY src/train.py knn
COPY src/datasets knn/datasets

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/knn

ENTRYPOINT [ "python", "train.py" ]