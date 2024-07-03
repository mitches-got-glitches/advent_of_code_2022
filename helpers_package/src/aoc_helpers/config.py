from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="AOC",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
    validators=[Validator("TEST", default=False, cast=bool)],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
