
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY . /app

# (Optional) install dependencies if you add any to requirements.txt
RUN if [ -s requirements.txt ]; then pip install -r requirements.txt; fi

# default command drops you into a shell; see README_DOCKER.md for examples
CMD ["/bin/bash"]
