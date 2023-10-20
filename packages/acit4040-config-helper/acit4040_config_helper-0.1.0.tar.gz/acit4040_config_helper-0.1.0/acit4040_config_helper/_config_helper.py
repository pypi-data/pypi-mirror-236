import os
import typing as t
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from google.api_core import exceptions as gcp_exceptions
from google.cloud import secretmanager

load_dotenv()


@lru_cache(maxsize=128)
def _get_secret_manager_raw(resource_name: str) -> bytes:
    """
    Access the payload of the given secret version if one exists.

    :param name: The name of the secret version to access.

    :return: The payload of the secret version.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Access the secret version.
    response = client.access_secret_version(name=resource_name)

    # Return the decoded payload of the secret version.
    return response.payload.data


def _clear_access_secret_version_cache() -> None:
    _get_secret_manager_raw.cache_clear()


def get_envvar_str(envvar_name: str, default_value: str | None = None) -> str:
    """
    Get the value of an environment variable as a string.

    Args:
        envvar_name (str): The name of the environment variable.
        default_value (str, optional): The default value to return if the
            environment variable is not set. Defaults to None.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set. A value of
            length zero is treated as not set.
    """
    contents = os.getenv(envvar_name, default_value)
    if contents is None or len(contents) == 0:
        raise ValueError(f"{envvar_name} is not set")
    return contents


def get_envvar_int(envvar_name: str, default_value: int | None = None) -> int:
    """
    Get the value of an environment variable as an integer.

    Args:
        envvar_name (str): The name of the environment variable.
        default_value (int, optional): The default value to return if the
            environment variable is not set. Defaults to None.

    Returns:
        int: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set or is not an integer.
    """
    contents = get_envvar_str(envvar_name, str(default_value))
    try:
        return int(contents)
    except Exception as e:
        raise ValueError(f"{envvar_name} is not an integer: {contents}") from e


def get_envvar_path(envvar_name: str, check_exists: bool = True) -> Path:
    """
    Get the path from an environment variable.

    Args:
        envvar_name (str): The name of the environment variable.
        check_exists (bool): Whether to check if the path exists. Defaults to True.

    Returns:
        Path: The path object.

    Raises:
        ValueError: If the environment variable is not a valid path.
        FileNotFoundError: If the path does not exist and check_exists is True.
    """
    path_str = get_envvar_str(envvar_name)
    try:
        path = Path(path_str)
    except Exception as e:
        raise ValueError(f"{envvar_name} is not a valid path: {path_str}") from e

    if check_exists and not path.exists():
        raise FileNotFoundError(f"{envvar_name} does not exist at path {path}")

    return path


def _get_secret_manager_file(
    secret_manager_resource_name: str,
    file_path: Path,
) -> Path:
    """
    Downloads a file from Google Cloud Secret Manager and writes it to the
    specified file path.

    Args:
        secret_manager_resource_name (str): The name of the secret resource in
            Google Cloud Secret Manager.
        file_path (Path): The file path to write the downloaded file to.

    Returns:
        Path: The file path of the downloaded file.
    """
    file_contents = _get_secret_manager_raw(secret_manager_resource_name)

    if not isinstance(file_contents, bytes):
        raise TypeError(f"Expected bytes, got {type(file_contents)}")

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_contents)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Failed to write secret manager file to {file_path}"
            )

        file_path.chmod(0o600)
    except FileNotFoundError as fnfe:
        raise fnfe

    return file_path


def get_secret(
    env_var_name: str,
    fallback_env_var_name: t.Optional[str] = None,
) -> str:
    """
    Retrieves a secret from the secret manager.

    Args:
        env_var_name (str): The name of the environment variable containing the secret name.
        fallback_env_var_name (Optional[str]): The name of the fallback environment variable
            containing the secret name.

    Returns:
        str: The secret value.

    Raises:
        ValueError: If the secret cannot be retrieved and no fallback is provided.
    """
    try:
        secret_name = get_envvar_str(env_var_name)
        return _get_secret_manager_raw(secret_name).decode("utf-8")
    except (gcp_exceptions.PermissionDenied, gcp_exceptions.NotFound):
        if fallback_env_var_name is None:
            raise ValueError(
                f"Failed to get secret {env_var_name} and no fallback provided"
            )
        return get_envvar_str(fallback_env_var_name)


def get_secret_file(
    env_var_name: str,
    output_file: Path,
    fallback_env_var_name: t.Optional[str] = None,
) -> Path:
    """
    Retrieves a secret file from the secret manager using the specified
    environment variable name.

    Args:
        env_var_name (str): The name of the environment variable
            containing the secret name.
        output_file (Path): The path to save the secret file to.
        fallback_env_var_name (Optional[str], optional): The name of
            the fallback environment variable containing the secret
            name. Defaults to None.

    Returns:
        Path: The path to the secret file.
    """
    try:
        secret_name = get_envvar_str(env_var_name)
        return _get_secret_manager_file(secret_name, output_file)
    except (gcp_exceptions.PermissionDenied, gcp_exceptions.NotFound):
        if fallback_env_var_name is None:
            raise ValueError(
                f"Failed to get secret {env_var_name} and no fallback provided"
            )

        return get_envvar_path(fallback_env_var_name, check_exists=True)
