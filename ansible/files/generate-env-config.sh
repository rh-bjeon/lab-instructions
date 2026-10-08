#!/bin/sh
# Generates docs/env-config.js from the container's environment variables so the
# docsify site (docs/index.html) can prefill <USER_NAME>/<PASSWORD>/<CLUSTER_DOMAIN>/<GIT_SERVER>
# without the student having to type them into the form at the top of the page.
set -eu

OUT_FILE="/opt/app-root/src/env-config.js"

escape_js() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'
}

{
  printf 'window.__ENV__ = {\n'
  if [ -n "${user:-}" ]; then
    printf '  USER_NAME: "%s",\n' "$(escape_js "$user")"
  fi
  if [ -n "${password:-}" ]; then
    printf '  PASSWORD: "%s",\n' "$(escape_js "$password")"
  fi
  if [ -n "${openshift_cluster_ingress_domain:-}" ]; then
    printf '  CLUSTER_DOMAIN: "%s",\n' "$(escape_js "$openshift_cluster_ingress_domain")"
  fi
  if [ -n "${gitea_console_url:-}" ]; then
    printf '  GIT_SERVER: "%s",\n' "$(escape_js "$gitea_console_url")"
  fi
  printf '};\n'
} > "$OUT_FILE"

echo "Generated $OUT_FILE"
