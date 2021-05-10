FROM python:3.9
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN ["python", "-m", "pip" , "install", "-r", "requirements.txt"]
CMD ["/bin/bash"]
