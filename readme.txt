## INSTALL DEPENDENCIES
pip install -r requirements.txt

## SERVER LOCAL
uvicorn main:app --reload

## SERVER PRODUCTION
pyinstaller main.spec

