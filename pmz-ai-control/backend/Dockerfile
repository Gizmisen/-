FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY run_pmz.py ./run_pmz.py
CMD ["python", "run_pmz.py"]
