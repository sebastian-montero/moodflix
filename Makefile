

run:
	git pull
	git lfs pull
	docker compose down
	docker compose up --build -d