FROM python:3.7.2-slim

WORKDIR /root/
COPY healthPod.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "healthPod.py"]
