#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== simulateurs-portail-elec — deploy ==="

echo "→ git pull"
git pull --ff-only

echo "→ docker compose build"
docker compose -f docker-compose.yml -f docker-compose.prod.yml build

echo "→ docker compose up -d (recreate)"
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans

echo "→ docker image prune"
docker image prune -f

echo "=== Deploy done — https://simu-elec.bercy.matge.com ==="
