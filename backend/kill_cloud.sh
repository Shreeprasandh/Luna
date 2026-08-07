#!/usr/bin/env bash
# Cloud Run Kill Switch — Sets minimum instances to 0 and stops incoming traffic
set -e

SERVICE_NAME="luna-backend"
REGION="asia-south1"

echo "=========================================="
echo "    KILLING CLOUD RUN SERVICE ($SERVICE_NAME)"
echo "=========================================="

gcloud run services update $SERVICE_NAME \
  --region=$REGION \
  --min-instances=0 \
  --max-instances=0

echo "Cloud Run service killed — 0 compute instances active."
