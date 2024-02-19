import dotenv


DEFAULT_ENV_FILE = ".env"


def load_env_file(env_path: str = DEFAULT_ENV_FILE):
    dotenv.load_dotenv(env_path, override=True)


def get_env_file_variables(env_path: str = DEFAULT_ENV_FILE):
    return dotenv.dotenv_values(env_path)


def update_env_file(values: dict, env_path: str = DEFAULT_ENV_FILE):
    for k, v in values.items():
        dotenv.set_key(env_path, k, v)
