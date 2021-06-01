FROM python:3.9
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY ./dist/ ./dist/

RUN pip install ./dist/parser_agent-0.0.2-py3-none-any.whl