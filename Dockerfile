FROM python:3.9

RUN ["useradd", "-m", "developer"]
WORKDIR /usr/src/app

RUN ["chown", "developer", "/usr/src/app"]
COPY --chown=developer:developer . /usr/src/app

USER developer
RUN ["python", "-m", "pip" , "install", "-r", "requirements.txt"]

ENTRYPOINT ["bash", "entrypoint.sh"]
