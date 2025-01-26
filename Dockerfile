FROM python:3.12-slim

WORKDIR /TEST_PROJECT

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["./start.sh"]

EXPOSE 8080