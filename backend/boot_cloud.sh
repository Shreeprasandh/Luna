#!/usr/bin/env bash
# Cloud Run Boot Switch — Restores Cloud Run deployment traffic to 100%
set -e

SERVICE_NAME="luna-backend"
REGION="asia-south1"

echo "=========================================="
echo "    BOOTING CLOUD RUN SERVICE ($SERVICE_NAME)"
echo "=========================================="

gcloud run services update $SERVICE_NAME \
  --region=$REGION \
  --to-latest \
  --async

echo "Cloud Run service traffic restored to 100%."
