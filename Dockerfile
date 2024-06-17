# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code/
COPY . /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt

# Expose port 8000 to allow communication to/from server
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
