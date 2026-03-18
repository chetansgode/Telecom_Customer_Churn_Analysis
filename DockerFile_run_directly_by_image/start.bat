@echo off
echo Starting Docker containers...

docker-compose -f docker-compose.yml -p project-2-telecom-customer-churn up -d
timeout /t 5

start http://localhost:8501
start http://localhost:8000/docs

pause