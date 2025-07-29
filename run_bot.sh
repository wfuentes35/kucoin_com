#!/bin/bash
set -e
while true; do
  source .env
  python main.py
  code=$?
  if [[ $code -ne 0 ]]; then
    sleep 1
  else
    break
  fi
done
