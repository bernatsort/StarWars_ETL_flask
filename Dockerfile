FROM python:3.11-slim

# Update the package repository and install dependencies
RUN apt-get update && \
    apt-get install -y build-essential

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip3 install -r requirements.txt

# Run app.py when the container launches
CMD ["python3", "src/app.py"]
 



