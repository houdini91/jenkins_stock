FROM python:3.8.3
LABEL stock_analyzer https://github.com/houdini91/jenkins_stock/stock_analyzer.git

WORKDIR /usr/src/stock

RUN mkdir -p /usr/src/stock
COPY dist /usr/src/stock
RUN ls -lh
RUN pwd
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install $(find . -name trans_jenkins-*.whl)


# CMD ["python", "./simple.py"]
