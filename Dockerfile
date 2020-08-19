# CLion remote docker environment (How to build docker container, run and stop it)
#
# Build and run:
#   docker build -t vldb -f Dockerfile .
#   docker run -d --cap-add sys_ptrace -p 2222:22 -p 8080:8080 -v "$(pwd):/project" --name vldb vldb
#   docker start vldb
#   docker exec -it vldb bash
#   ssh-keygen -f "$HOME/.ssh/known_hosts" -R "[localhost]:2222"
#
# stop:
#   docker stop vldb
#
# 
# ssh credentials (test user):
#   user@password 

FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y ssh \
      build-essential \
      gcc \
      g++ \
      gdb \
      clang \
      cmake \
      rsync \
      tar \
      python3 \
      python3-dev \
      python3-pip \
      software-properties-common \
  && add-apt-repository -y ppa:deadsnakes/ppa \
  && apt-get update \
  && apt-get -y install python3.5 python3.5-dev \
  && apt-get clean

RUN python3.5 -m pip install numpy pandas scipy scikit-learn tensorflow==1.15 networkx==1.10 beautifulsoup4 lxml matplotlib seaborn colour pytz requests flask
RUN pip3 install numpy pandas scipy scikit-learn tensorflow==1.15 networkx==1.10 beautifulsoup4 lxml matplotlib seaborn colour pytz requests flask
RUN ( \
    echo 'LogLevel DEBUG2'; \
    echo 'PermitRootLogin yes'; \
    echo 'PasswordAuthentication yes'; \
    echo 'Subsystem sftp /usr/lib/openssh/sftp-server'; \
  ) > /etc/ssh/sshd_config_vldb \
  && mkdir /run/sshd

RUN useradd -m user \
  && yes password | passwd user

CMD ["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config_vldb"]

WORKDIR /project

