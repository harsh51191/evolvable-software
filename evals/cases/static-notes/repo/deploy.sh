#!/bin/sh
# Usage: ./deploy.sh v1.4.0   (run on the host by the on-call engineer)
set -eu
TAG="$1"
docker pull "ghcr.io/example/static-notes:$TAG"
docker rm -f static-notes || true
docker run -d --name static-notes -p 8080:8080 -v notes-data:/data "ghcr.io/example/static-notes:$TAG"
