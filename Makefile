install:
	# Required to pull package from Azure DevOps Artifacts
	pip install keyring artifacts-keyring
	pipenv install -d
	pipenv shell || echo "Continuing"

test:
	./spark-on-lambda/test.sh

code:
	black dl_light_containers --check
	flake8 dl_light_containers
	# mypy dl_light_containers

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete