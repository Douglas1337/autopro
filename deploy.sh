#!/bin/bash

# Configurações
REMOTE_USER="autopro"
REMOTE_HOST="127.0.0.1"
REMOTE_PORT=2223
REMOTE_DIR="/home/autopro/"

# Comando rsync com exclusões e porta customizada
rsync -avz --delete \
  -e "ssh -p ${REMOTE_PORT}" \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '*.pyo' \
  --exclude '*.log' \
  ./ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}

# Verificação de status
if [ $? -eq 0 ]; then
  echo "✅ Deploy concluído com sucesso para ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR} (porta ${REMOTE_PORT})"
else
  echo "❌ Ocorreu um erro durante o deploy"
fi
