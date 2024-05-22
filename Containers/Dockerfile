FROM python:3.10

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/anastmur/advanced_paper_analyzer

RUN apt-get update && apt-get install -y curl

RUN apt-get update && apt-get install -y python3

RUN set -xe
RUN curl -sSL https://install.python-poetry.org | python3 - --git https://github.com/python-poetry/poetry.git@main
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /advanced_paper_analyzer

RUN poetry install
WORKDIR /advanced_paper_analyzer/Scripts

# Set up VNC server
RUN mkdir -p ~/.vnc
RUN echo "pw123" | vncpasswd -f > ~/.vnc/passwd
RUN chmod 600 ~/.vnc/passwd
RUN echo '#!/bin/bash\nxrdb $HOME/.Xresources\nstartxfce4 &' > ~/.vnc/xstartup
RUN chmod +x ~/.vnc/xstartup

# Expose the VNC port
EXPOSE 8060

# Start VNC server and run the GUI application
CMD ["sh", "-c", "vncserver :1 -geometry 1280x800 -depth 24 && python /advanced_paper_analyzer/Scripts/interface.py"]