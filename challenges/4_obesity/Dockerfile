FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /usr/src/app

COPY . .

RUN uv sync --locked --no-dev

CMD ["uv",  "run",  "streamlit",  "run",  "code/streamlit/app.py"]


