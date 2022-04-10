export PYTHONPATH := .

ve:
	python3 -m venv .ve; \
	. .ve/bin/activate; \
	pip install -r requirements.txt; \

clean:
	test -d .ve && rm -rf .ve

runserver:
	 uvicorn main.app:app --host 0.0.0.0 --port 5000 --reload

install_hooks:
	pip install -r requirements-ci.txt; \
	pre-commit install; \

run_hooks_on_all_files:
	pre-commit run --all-files

style:
	flake8 main

types:
	mypy --namespace-packages -p "main" --config-file setup.cfg

migration:
	alembic revision --autogenerate -m "$(message)"

migrate:
	alembic upgrade head
