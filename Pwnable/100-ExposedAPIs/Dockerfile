FROM python:2.7-alpine

RUN addgroup -S p100 && adduser -S -h /ctf-p100 -s /bin/false -G p100 p100

COPY ./requirements.txt /ctf-p100/
RUN pip install --no-cache-dir -r /ctf-p100/requirements.txt

COPY ./src /ctf-p100/src/
WORKDIR /ctf-p100

EXPOSE 30877

USER p100
CMD ["python", "src/app.py", "--listen=0.0.0.0:30877"]
