# Use the official Python runtime image
FROM ghcr.io/astral-sh/uv:python3.14-trixie
 
# Create the app directory
RUN mkdir /app
 
WORKDIR /app
 
ENV PYTHONUNBUFFERED=1 
ENV UV_COMPILE_BYTECODE=1

ADD --unpack=true source.tar /app
 
# Expose the Django port
EXPOSE 8000
 
RUN <<EOF
uv run manage.py tailwind install
uv run manage.py tailwind build
EOF

ENTRYPOINT ["./entrypoint.sh"]
