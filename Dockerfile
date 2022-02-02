FROM python:3.8.12 as base_image
EXPOSE 8080

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
    && apt-get upgrade -y

RUN useradd -ms /bin/bash devsocial

WORKDIR /home/devsocial
COPY requirements.txt .

RUN chown -R devsocial:devsocial /home/devsocial \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install -r requirements.txt

COPY . .

RUN chown -R devsocial:devsocial /home/devsocial

# **************************** Dev pod
FROM base_image as dev
USER root

# run server
CMD ["python3", "runserver.py"]


# **************************** Dev pod
FROM base_image as prod

USER root

# Removing tools used by adversaries. Hardening
ENV SUDO_FORCE_REMOVE=yes
RUN apt-get --purge remove -y --allow-remove-essential curl wget sudo
RUN dpkg -r --force-all apt
RUN dpkg -r --force-all debconf dpkg

USER devsocial
WORKDIR  /home/devsocial

# run server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "runserver:app"]
