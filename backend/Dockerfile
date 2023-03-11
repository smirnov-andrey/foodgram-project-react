FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY ./foodgram .
COPY .env .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]