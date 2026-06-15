.PHONY: help up down restart build logs test clean-test clean migrate revision

help:
	@echo Comandos disponiveis:
	@echo   make up        Sobe app e banco em segundo plano
	@echo   make down      Para app e banco mantendo volumes
	@echo   make restart   Reinicia app e banco
	@echo   make build     Recria a imagem Docker
	@echo   make logs      Acompanha logs do app
	@echo   make test      Sobe banco de teste, roda testes e remove dados de teste
	@echo   make migrate   Aplica migrations no banco principal
	@echo   make revision  Cria migration vazia: make revision msg="mensagem"
	@echo   make clean     Para app e banco removendo volumes

up:
	docker compose up -d

down:
	docker compose down

restart: down up

build:
	docker compose build

logs:
	docker compose logs -f app

test:
	docker compose --profile test up -d postgres_test
	@trap 'docker compose --profile test rm -sfv postgres_test' EXIT; docker compose --profile test run --rm app_test

clean-test:
	docker compose --profile test rm -sfv postgres_test app_test

clean:
	docker compose down -v

migrate:
	docker compose run --rm app alembic upgrade head

revision:
ifndef msg
	$(error Use: make revision msg="mensagem")
endif
	docker compose run --rm app alembic revision -m "$(msg)"
