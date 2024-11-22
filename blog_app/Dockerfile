FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/app

# For installation dependencies with pip
# COPY ./requirements.txt ./requirements.txt
# RUN pip install -U pip setuptools \
#     && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -U pip setuptools \
    && pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

EXPOSE 8000

ENTRYPOINT [ "python", "-m", "main" ]
