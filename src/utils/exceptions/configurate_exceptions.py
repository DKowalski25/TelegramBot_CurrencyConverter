class ConfigurateExceptions(ValueError):
    """Parent exception for all errors with any program configuration."""


class EnvDependNotFound(ConfigurateExceptions):
    """Exception: .env variables not found."""

    def __init__(self, depend_name: str):
        err_str = f'Not found depend name: {depend_name}'
        super.__init__(err_str)