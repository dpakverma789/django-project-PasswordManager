echo "======> INSTALLING REQUIREMENTS <======"
pip install -r requirements.txt
echo "======> REQUIREMENTS INSTALLED <======"

echo "======> COLLECTING STATIC FILES <======"
python3 manage.py collectstatic --noinput
echo "======> STATIC FILES COLLECTED <======"

