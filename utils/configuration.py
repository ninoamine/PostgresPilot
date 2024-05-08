import os


def postgresql_url_env():
    result = os.environ.get("POSTGRESQL_URL")
    if result is None or not result:
        return False
    return result

        