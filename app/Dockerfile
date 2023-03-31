# app/Dockerfile

# fetch python official image from Docker Hub
FROM python:3.9-slim
# create a /app directory to be the working directory
WORKDIR /app
# copy everything inside /app locally to the /app folder inside the container
# (this is already working director, hence the .)
COPY . .
# install the requirements
RUN pip install -r requirements.txt

# needs to expose port to see streamlit application (by default streamlit uses 8501)
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
# this makes the container run on top of the built image as executable
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]