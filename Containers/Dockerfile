FROM python:3.10

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/anastmur/advanced_paper_analyzer

RUN apt-get update && apt-get install -y curl

RUN apt-get update && apt-get install -y python3

RUN set -xe
RUN curl -sSL https://install.python-poetry.org | python3 - --git https://github.com/python-poetry/poetry.git@main
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /advanced_paper_analyzer

RUN poetry install
WORKDIR /advanced_paper_analyzer/Scripts

EXPOSE 8060

CMD ["python", "interface.py"]
