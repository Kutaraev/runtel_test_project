#!/bin/sh

alembic upgrade head

python data_loader.py

python main.py