# syntax=docker/dockerfile:1

# FROM python:3.10.5-slim-buster

# WORKDIR /code

# # 
# COPY ./requirements.txt /code/requirements.txt

# # 
# RUN pip install --upgrade pip

# RUN python3 -m pip install --no-cache-dir --upgrade \
#   setuptools \
#   wheel \
#   && \
#   python3 -m pip install --trusted-host pypi.python.org -r /code/requirements.txt

# COPY ./app /code/app  

# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--reload"]

FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip  
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt