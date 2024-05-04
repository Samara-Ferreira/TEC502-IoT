
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install Flask

EXPOSE 5555
EXPOSE 5551
EXPOSE 5552/udp

CMD ["python", "api_broker.py"]