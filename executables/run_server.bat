@REM  SET ENVIRONMENT
SET WEB_SERVER_HOST="127.0.0.1"
SET WEB_SERVER_PORT=8000
SET PYTHONPATH=C:\Users\Ramkumar.E\Documents\web_server\src

@REM  ACTIVATE VENV
CALL C:\Users\Ramkumar.E\Documents\web_server\.venv\Scripts\activate.bat
@REM  RUN SERVER
python -m web_server
