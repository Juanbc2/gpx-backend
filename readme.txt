uvicorn main:app --reload

pyinstaller -F main.py --clean

pyinstaller main.spec

