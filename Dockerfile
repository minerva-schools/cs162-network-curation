###
FROM python:3-alpine
COPY requirements.txt .

# Set the working directory to /web
WORKDIR /web

# Copy the current directory contents into the container at /web
ADD . /web
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "-m", "flask", "run"]