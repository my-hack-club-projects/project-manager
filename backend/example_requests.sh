#!/bin/bash

BASE_URL="http://localhost:8000/api"  # Replace with your Django API base URL
USERNAME="test_user"
PASSWORD="password"  # Replace with the test user's password

# Obtain authentication token
echo "Logging in as $USERNAME..."

TOKEN=$(curl -s -X POST "$BASE_URL/token/login/" -H "Content-Type: application/json" -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" | jq -r .token)

if [ -z "$TOKEN" ]; then
  echo "Failed to obtain authentication token."
  exit 1
fi

echo "Authentication successful. Token: $TOKEN"

# Fetch all categories
echo "Fetching categories..."
curl -s -X GET "$BASE_URL/categories/" -H "Authorization: Token $TOKEN" | jq .

echo "Categories fetched successfully."
