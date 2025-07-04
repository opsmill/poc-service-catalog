# Use an official Python base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.create false

COPY . /app

# Install dependencies
RUN poetry install

# Copy the rest of the application

# Expose the port Streamlit uses
EXPOSE 8501

# Run the application
CMD ["poetry", "run", "streamlit", "run", "service_catalog/🏠_Home_Page.py"]