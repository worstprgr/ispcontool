FROM debian:latest
LABEL authors="adam@seishin.dev"
MAINTAINER shl

RUN apt-get update

# Set timezone
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# Install things
RUN apt install -y python3

# Utils
RUN apt install -y nano

# Project Paths
ENV dWDIR=/ispcontool/

# Project Vars
ENV TIME_INTERVAL=8
ENV TIME_MODE=D
ENV TIME_TOLERANCE=5
ENV MAIN_ROUTINE_SLEEP=60
ENV SUB_ROUTINE_SLEEP=60
ENV SUB_RATE=1

# Project prep
COPY . $dWDIR

# Project permissions
RUN chmod -R u+rwx $dWDIR

WORKDIR $dWDIR

RUN python3 './setup.py'

CMD ["python3", "-u", "/ispcontool/main.py"]
