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
ENV dCORE=${dWDIR}core/
ENV sCORE=/core

# Project Vars
ENV BASE_DIR=$dWDIR
ENV TIME_INTERVAL=8
ENV TIME_MODE=D
ENV TIME_TOLERANCE=5
ENV MAIN_ROUTINE_SLEEP=60
ENV SUB_ROUTINE_SLEEP=60
ENV SUB_RATE=1

# Project prep
COPY main.py $dWDIR
COPY $sCORE/config.py $dCORE
COPY $sCORE/cfg_default.py $dCORE
COPY $sCORE/cfg_docker.py $dCORE
COPY $sCORE/datautils.py $dCORE
COPY $sCORE/exceptions.py $dCORE
COPY $sCORE/fileutils.py $dCORE
COPY $sCORE/logger.py $dCORE
COPY $sCORE/mocks.py $dCORE
COPY $sCORE/portutils.py $dCORE
COPY $sCORE/signalutils.py $dCORE
COPY $sCORE/timeutils.py $dCORE

# Project permissions
RUN chmod -R u+rwx $dWDIR

WORKDIR $dWDIR

CMD ["python3", "-u", "/ispcontool/main.py"]
