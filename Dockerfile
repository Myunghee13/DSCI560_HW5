FROM python:3

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5006

CMD ["bokeh", "serve", "--allow-websocket-origin=ip172-18-0-59-buiecm1qckh000ecb3og-5006.direct.labs.play-with-docker.com", "./app.py"]
