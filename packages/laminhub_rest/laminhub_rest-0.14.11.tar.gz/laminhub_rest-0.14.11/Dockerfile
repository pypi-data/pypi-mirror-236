FROM --platform=linux/amd64 python:3.9
WORKDIR /laminhub-rest
COPY . /laminhub-rest
RUN pip install --upgrade .[server]
ENTRYPOINT ./scripts/run.sh
