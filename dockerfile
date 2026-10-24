FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY pyproject.toml ./
RUN uv sync

COPY . .

EXPOSE 8787

CMD ["uv", "run", "pywrangler", "dev", "--ip", "0.0.0.0", "--port", "8787", "--inspector-port", "9229"]