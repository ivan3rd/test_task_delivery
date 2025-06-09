#!/bin/sh
while true; do
  curl -X PUT http://backend:8000/package/set-delivery-cost
  sleep 1800
done
