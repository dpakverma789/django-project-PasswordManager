echo "======> INSTALLING REQUIREMENTS <======"
pip install -r requirements.txt
echo "======> REQUIREMENTS INSTALLED <======"

echo "======> COLLECTING STATIC FILES <======"
python manage.py collectstatic --noinput --clear
echo "======> STATIC FILES COLLECTED <======"

