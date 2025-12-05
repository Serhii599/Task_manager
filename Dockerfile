FROM python:3.12
ADD . /src
WORKDIR /scr
RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt