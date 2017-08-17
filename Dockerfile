FROM python:alpine3.6
WORKDIR /usr/src/app
COPY ./main.py .
RUN pip install cqlsh
CMD [ "python", "./main.py" ]
