# Use the official Python runtime image
FROM ghcr.io/astral-sh/uv:python3.14-trixie

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# Create the app directory
RUN mkdir /app
 
WORKDIR /app
 
ENV PYTHONUNBUFFERED=1 
ENV UV_COMPILE_BYTECODE=1

ADD --unpack=true source.tar /app
 
# Expose the Django port
EXPOSE 8000

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install base dependencies
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

ENV NVM_DIR /usr/local/nvm # or ~/.nvm , depending
ENV NODE_VERSION 0.10.33

# Install nvm with node and npm
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.20.0/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/v$NODE_VERSION/bin:$PATH


RUN <<EOF
uv run manage.py tailwind install
uv run manage.py tailwind build
EOF

ENTRYPOINT ["./entrypoint.sh"]
