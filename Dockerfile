FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY *.py /app/
COPY strategies /app/strategies
COPY demos /app/demos
COPY validators /app/validators
COPY tests /app/tests
COPY pytest.ini /app/pytest.ini
CMD ["python", "-m", "pytest", "-q"]
