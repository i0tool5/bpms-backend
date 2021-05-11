#!/bin/sh

sh -c 'python -m daphne -b 0.0.0.0 bpms.asgi:application'
