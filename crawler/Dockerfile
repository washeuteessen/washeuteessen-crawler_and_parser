FROM python:3.7
COPY . /crawler
RUN chmod 777 -R crawler
RUN pip install --no-cache-dir -r /crawler/requirements.txt --trusted-host pypi.org
WORKDIR /
CMD [ "python", "./start_crawler.py" ]