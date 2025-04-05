docker-compose down -v
docker-compose up -d --build

Write-Host "⏳ Waiting 20 seconds for DB initialization..."
Start-Sleep -Seconds 20

Write-Host "🚀 Executing Alembic migrations..."
docker exec contacts_app poetry run alembic upgrade head

Write-Host "⏳ Waiting 5 seconds after migration..."
Start-Sleep -Seconds 5

Write-Host "🌱 Seeding database..."
docker exec contacts_app poetry run python src/seeds.py

Write-Host "✅ Setup complete: containers running, migrations applied, database seeded."
