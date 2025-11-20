# Use the official Python runtime image
FROM ghcr.io/astral-sh/uv:python3.14-trixie

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# Create the app directory
RUN mkdir /app
 
WORKDIR /app
 
ENV PYTHONUNBUFFERED=1 
ENV UV_COMPILE_BYTECODE=1

ADD . /app
 
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


# Install nvm with node and npm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

RUN <<EOF
\. "$HOME/.nvm/nvm.sh"
nvm install 24
uv run manage.py tailwind install
uv run manage.py tailwind build
EOF

ENTRYPOINT ["/app/entrypoint.sh"]
