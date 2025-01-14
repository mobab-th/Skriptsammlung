FROM ubuntu:jammy
LABEL maintainer="mobab"

ARG dissectRELEASE=3.17.1
ARG flowrecordRELEASE=3.18
ARG acquireRELEASE=3.17

# Create container with:
# podman  build -f dissect.dockerfile -t dissect:3.17.1 .
#
# podman run --rm --name dissect --hostname dissect -v /media:/media/ -v $HOME:$HOME localhost/dissect:3.17.1 target-query Befehlskette
# oder interaktiv in der bash
# podman run -it --rm --name dissect --hostname dissect -v /media:/media/ -v $HOME:$HOME localhost/dissect:3.17.1 /bin/bash
# Container starten mit Möglichkeit zum Mounten

#    podman run -it --userns=keep-id:uid=1000 --rm --device /dev/fuse -v /etc/fuse.conf:/etc/fuse.conf:ro --cap-add SYS_ADMIN -v /media:/media -v $HOME:$HOME localhost/dissect:3.17.1 /bin/bash




ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get -y update && \
    apt-get -y install apt-transport-https apt-utils && \
    apt-get -y install libterm-readline-gnu-perl software-properties-common && \
    apt-get -y install locales python3-pip-whl python3-pip && \
    apt-get -y install screen mc && \
    apt-get -y install libfuse2 fuse && \
    apt-get -y upgrade
RUN apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/*

# dissect von PyPi.org
RUN pip3 install --no-cache-dir dissect==${dissectRELEASE} && \
    pip3 install --no-cache-dir flow.record==${flowrecordRELEASE} && \
    pip3 install --no-cache-dir acquire==${acquireRELEASE} && \
    pip3 install --no-cache-dir openpyxl && \
    pip3 install --no-cache-dir tabulate && \
    pip3 install --no-cache-dir cursor && \
    pip3 install --no-cache-dir colorama && \
    pip3 install --no-cache-dir logger_color && \
    pip3 install --no-cache-dir progressbar2

# Set terminal to UTF-8 by default
RUN locale-gen de_DE.UTF-8 && update-locale LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8
ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8


