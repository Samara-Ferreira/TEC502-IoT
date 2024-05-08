
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install Flask

EXPOSE 5575
EXPOSE 5571
EXPOSE 5572/udp

CMD ["python", "main_api.py"]