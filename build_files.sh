#!/bin/bash

# Install pip if not available
if ! command -v pip &> /dev/null
then
    echo "pip not found, installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py --user
fi

# Activate virtual environment (if necessary)
python -m venv venv
source venv/bin/activate

echo "======> INSTALLING REQUIREMENTS <======"
pip install -r requirements.txt
echo "======> REQUIREMENTS INSTALLED <======"

echo "======> COLLECTING STATIC FILES <======"
python3.9 manage.py collectstatic --noinput --clear
echo "======> STATIC FILES COLLECTED <======"

echo "======> MAKE-MIGRATIONS <======"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
echo "======> MAKE-MIGRATIONS-END <======"
