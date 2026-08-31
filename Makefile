.PHONY: help up down restart build logs test clean-test clean migrate revision seeder

help:
	@echo Comandos disponiveis:
	@echo   make up        Sobe app e banco em segundo plano
	@echo   make down      Para app e banco mantendo volumes
	@echo   make restart   Reinicia app e banco
	@echo   make build     Recria a imagem Docker
	@echo   make logs      Acompanha logs do app
	@echo   make test      Sobe banco de teste, roda testes e remove dados de teste
	@echo   make migrate   Aplica migrations no banco principal
	@echo   make revision  Cria migration via autogenerate: make revision msg="mensagem"
	@echo   make seeder    Popula a base de demonstracao (todos os modulos + BI)
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

# --build e obrigatorio: sem ele o compose reusa a imagem antiga e uma dependencia
# nova em requirements.txt nao entra. Ja aconteceu — streamlit-aggrid ficou fora
# da imagem e os testes que dependiam dele passaram a ser PULADOS em silencio,
# enquanto o codigo que o usava so nao quebrava porque a base estava vazia.
test:
	docker compose --profile test up -d postgres_test
	@trap 'docker compose --profile test rm -sfv postgres_test' EXIT; docker compose --profile test run --rm --build app_test

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
	docker compose run --rm app alembic revision --autogenerate -m "$(msg)"

# app_seed ja roda automaticamente no "make up" (servico one-shot no compose);
# este alvo serve para rodar so o seed de novo sem tocar no app/Streamlit.
seeder:
	docker compose up -d postgres
	docker compose run --rm app_seed
