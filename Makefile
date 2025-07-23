build:
	docker build -t steambot:latest .
run:
	docker run -it -d --env-file .env --restart=unless-stopped --name steambot steambot --mount type=bind,source=$(pwd)/db/db.sqlite3,target=/usr/src/app/db.sqlite3
stop:
	docker stop steambot
attach:
	docker attach steambot
dell:
	docker rm steambot