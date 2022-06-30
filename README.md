# Create Venv
python -m venv venv
# Activate Venv
source venv/bin/activate (Linux)
venv/Scripts/Activate (Windows)

# Install requirements.txt
pip install -r requirements.txt

# Run main.py
uvicorn app.api:app --reload
or 
docker-compose up --build
or
run main.py file by vscode

# Run test
cd test
pip install -r requirements.txt
python3 -m unittest -v

# Api Documentation
http://127.0.0.1:8081/docs

# Run Python code formatter with black
black .
or black app
or bkacl tests

# Routes

curl --request POST \
  --url http://127.0.0.1:8081/token \
  --data '{"username": "teste", "password": "teste"}'

curl --request GET \
  --url http://127.0.0.1:8081/users \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZGlwbzMiLCJleHAiOjE2NTY1NDg0Mzl9.fdc0cxfSTiciMuJOc0oRP_UKdt3UapwpIGYmXlaYyHw' \
  --header 'Content-Type: application/json' \
  --data '{
		"username": "example",
		"password": "password"
}'

curl --request POST \
  --url http://127.0.0.1:8081/user \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZGlwbzMiLCJleHAiOjE2NTY0NjYzNTV9.md21STMa6IhhaR2vUP601VhN16GnK5mjE6jBTarRIBU' \
  --header 'Content-Type: application/json' \
  --data '{
		"uuid": "2",
		"username": "teste2",
		"password": "teste2"
	}'

curl --request GET \
  --url http://127.0.0.1:8081/patients \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZGlwbzMiLCJleHAiOjE2NTY1NDg0Mzl9.fdc0cxfSTiciMuJOc0oRP_UKdt3UapwpIGYmXlaYyHw' \
  --header 'Content-Type: application/json'

curl --request GET \
  --url 'http://127.0.0.1:8081/patients?first_name=JOANA' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZGlwbzMiLCJleHAiOjE2NTY1NTAyNDd9.WqcEnaTRySbe-m_3JQdm6Lka0YMX4H3xmzcUIWgtr7A' \
  --header 'Content-Type: application/json'

curl --request GET \
  --url http://127.0.0.1:8081/pharmacies \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZGlwbzMiLCJleHAiOjE2NTY1NDg0Mzl9.fdc0cxfSTiciMuJOc0oRP_UKdt3UapwpIGYmXlaYyHw' \
  --header 'Content-Type: application/json'

curl --request GET \
  --url http://0.0.0.0:8081/transactions \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZGlwbzMiLCJleHAiOjE2NTY1NDg0Mzl9.fdc0cxfSTiciMuJOc0oRP_UKdt3UapwpIGYmXlaYyHw' \
  --header 'Content-Type: application/json'
