run:
	docker run -it -d --env-file .env --restart=unless-stopped --name steambot steambot
stop:
	docker stop steambot
attach:
	docker attach steambot
dell:
	docker rm steambot