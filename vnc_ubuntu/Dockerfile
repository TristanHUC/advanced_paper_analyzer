FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

ENV USER=root

# Install XFCE, VNC server, dbus-x11 and xorg
RUN apt-get update && apt-get install -y --no-install-recommends \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    dbus-x11 \
    xfonts-base \
    xorg \
    xfonts-75dpi \
    xfonts-100dpi \
    xfonts-scalable \
    xterm \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /root/.vnc \
    && echo "pw123" | vncpasswd -f > /root/.vnc/passwd \
    && chmod 600 /root/.vnc/passwd

RUN touch /root/.Xauthority

RUN echo "XTerm*faceName: Monospace" > /root/.Xresources

ENV RESOLUTION=1920x1080

WORKDIR /app

COPY start-vnc.sh start-vnc.sh
RUN chmod +x start-vnc.sh

WORKDIR /

RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    curl \
    python3 \
    python3-venv \
    python3-dev \
    python3-pip \
    python3-tk  # Ensure tkinter is installed

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev python3.10-tk

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

RUN curl -sSL https://install.python-poetry.org | python3.10 -

ENV PATH="/root/.local/bin:$PATH"

RUN git clone --recursive https://github.com/anastmur/advanced_paper_analyzer

WORKDIR /advanced_paper_analyzer

RUN poetry env use python3.10

RUN poetry install

WORKDIR /advanced_paper_analyzer

EXPOSE 5901

CMD ["bash", "../app/start-vnc.sh"]
