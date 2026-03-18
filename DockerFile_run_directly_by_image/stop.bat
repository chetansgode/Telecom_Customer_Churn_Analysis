@echo off
echo Stopping Docker containers...
docker-compose -f docker-compose.yml -p project-2-telecom-customer-churn down

pause