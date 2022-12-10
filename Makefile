install:
	# Required to pull package from Azure DevOps Artifacts
	pip install keyring artifacts-keyring
	pipenv install -d
	pipenv shell || echo "Continuing"

test:
	./spark3-on-lambda/test-local.sh

code:
	black . --check
	flake8 .
	# mypy .

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete