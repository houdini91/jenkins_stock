FROM python:3.8.3
LABEL stock_analyzer https://github.com/houdini91/jenkins_stock/stock_analyzer.git

WORKDIR /usr/src/stock

RUN mkdir -p /usr/src/stock
COPY requirements.txt /usr/src/stock/
RUN pip install -r requirements.txt

COPY dist /usr/src/stock/

ENV PYTHONUNBUFFERED 1
RUN pip install $(find . -name trans_jenkins-*.whl)

COPY py_trans_jenkins/trans_jenkins/examples /usr/src/stock/examples

# CMD ["python", "./simple.py"]
