docker compose up -f compose.local.yaml redis -d
docker compose up -f compose.local.yaml zapbackend -d
docker compose up -f compose.local.yaml zapfrontend -d