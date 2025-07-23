build:
	docker build -t steambot:latest .
run:
	docker run -it -d --env-file .env --restart=unless-stopped --name steambot steambot --volume /home/lynx/steam-pay-bot/db.sqlite3:/usr/src/app/db.sqlite3
stop:
	docker stop steambot
attach:
	docker attach steambot
dell:
	docker rm steambot