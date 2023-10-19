import logging

from BL_Python.database.config import DatabaseConfig
from BL_Python.database.dependency_injection import ScopedSessionModule
from BL_Python.programming.config import load_config
from injector import Injector
from pytest_mock import MockerFixture


def test__Config__load_config__initializes_database_config(mocker: MockerFixture):
    fake_config_dict = {"connection_string": "test_connection_string"}
    _ = mocker.patch("io.open")
    _ = mocker.patch("toml.decoder.loads", return_value=fake_config_dict)
    config = load_config(DatabaseConfig, "foo.toml")

    log = logging.getLogger()

    m = ScopedSessionModule()
    i = Injector(m)
    i.binder.bind(logging.Logger, to=log)

    assert config is not None
    assert config.connection_string == "test_connection_string"
