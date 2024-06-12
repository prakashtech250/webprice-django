echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all deps in the venv
pip install -r requirements.txt

# collect static files using the Python interpreter from venv
python manage.py collectstatic --noinput

python manage.py tailwind init
python manage.py tailwind install
python manage.py tailwind start

echo "BUILD END"

# [optional] Start the application here 
# python manage.py runserver