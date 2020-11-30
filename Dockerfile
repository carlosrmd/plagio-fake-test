FROM python:3.8.6-slim-buster

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY source /app
COPY configuration/defaults /app/configuration/defaults

WORKDIR /app

RUN chmod +x run.sh

ENTRYPOINT ["/bin/bash"]
CMD ["./run.sh"]