FROM python:3.7
COPY . /crawler
RUN chmod 777 -R crawler
RUN pip install --no-cache-dir -r /crawler/requirements.txt
WORKDIR /crawler/recipes
CMD [ "python", "./start.py" ]
