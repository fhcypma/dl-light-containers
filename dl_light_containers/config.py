from dynaconf import Dynaconf


settings = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",  # export envvars with `export DYNACONF_FOO=bar`.
    settings_files=["settings.yaml"],  # Load files in the given order.
    lowercase_read=True,
    load_dotenv=True,
)
