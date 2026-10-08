// Fallback for local `docsify serve` / GitHub Pages where no deployment env vars exist.
// When deployed on OpenShift, this file is overwritten at container start by
// ansible/files/generate-env-config.sh using the Deployment's env vars.
window.__ENV__ = {};
