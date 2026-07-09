#!/usr/bin/env bash
# curl-test.sh — tests the timeline_post API endpoints.
# Creates a random timeline post via POST, verifies it appears in GET,
# and (bonus) deletes it via the DELETE endpoint at the end.
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:5000}"
ENDPOINT="${BASE_URL}/api/timeline_post"

# --- create a random post -----------------------------------------------------
RANDOM_ID="$RANDOM$RANDOM"
NAME="TestUser${RANDOM_ID}"
EMAIL="test${RANDOM_ID}@example.com"
CONTENT="Automated test post ${RANDOM_ID}"

echo "==> POST ${ENDPOINT}"
POST_RESPONSE=$(curl -s -X POST "${ENDPOINT}" \
  -d "name=${NAME}" \
  -d "email=${EMAIL}" \
  -d "content=${CONTENT}")
echo "${POST_RESPONSE}"

# extract the new post's id from the JSON response (no jq dependency)
POST_ID=$(echo "${POST_RESPONSE}" | grep -o '"id": *[0-9]*' | grep -o '[0-9]*' | head -1)
if [[ -z "${POST_ID}" ]]; then
  echo "FAIL: POST did not return a post id"
  exit 1
fi
echo "==> created post id=${POST_ID}"

# --- verify it shows up in GET --------------------------------------------------
echo "==> GET ${ENDPOINT}"
GET_RESPONSE=$(curl -s "${ENDPOINT}")

if echo "${GET_RESPONSE}" | grep -q "${CONTENT}"; then
  echo "PASS: random post found in GET response"
else
  echo "FAIL: random post NOT found in GET response"
  echo "${GET_RESPONSE}"
  exit 1
fi

# --- bonus: clean up the test post via DELETE ----------------------------------
echo "==> DELETE ${ENDPOINT}/${POST_ID}"
DELETE_RESPONSE=$(curl -s -X DELETE "${ENDPOINT}/${POST_ID}")
echo "${DELETE_RESPONSE}"

# confirm it is gone
if curl -s "${ENDPOINT}" | grep -q "${CONTENT}"; then
  echo "FAIL: post still present after DELETE"
  exit 1
else
  echo "PASS: test post deleted — all tests passed"
fi
