#!/bin/sh
set -x

echo "=== start.sh: PORT=${PORT} ==="

# Copy static files to writable temp dir
mkdir -p /tmp/html
cp /app/index.html /tmp/html/index.html

# Generate config.js with tokens from environment variables
cat > /tmp/html/config.js << ENDOFCONFIG
window.AIRTABLE_TOKEN = '${AIRTABLE_TOKEN}';
window.ANTHROPIC_KEY = '${ANTHROPIC_KEY}';
ENDOFCONFIG

echo "=== config.js written, starting nginx on port 3000 ==="

# nginx.conf already has port 3000 and root /tmp/html hardcoded
exec nginx -g 'daemon off;' -c /app/nginx.conf
