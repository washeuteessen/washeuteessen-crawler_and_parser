# Define the base image used to start the build process
FROM python:3.7

# Copy content to docker container
COPY . /parser

# Central executing directive for Dockerfiles.
RUN chmod 777 -R parser
RUN pip install --no-cache-dir -r /parser/requirements.txt --trusted-host pypi.org

# Set the path where the command, defined with CMD, is to be executed.
WORKDIR /parser

# Execute a specific command within the container.
CMD [ "python", "start_parser.py" ]

# source for explanations: https://www.linode.com/docs/applications/containers/how-to-use-dockerfiles/