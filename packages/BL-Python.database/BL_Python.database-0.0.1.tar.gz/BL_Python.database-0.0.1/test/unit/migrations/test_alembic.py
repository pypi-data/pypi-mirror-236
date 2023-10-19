# TODO these are not functional until Alembic is supported.
# from configparser import ConfigParser
# from typing import Any, Type, cast
#
# from alembic.command import downgrade, upgrade
# from alembic.config import Config as AlembicConfig
# from injector import Injector
# from sqlalchemy import create_engine
# from sqlalchemy.engine import Engine
# from sqlalchemy.orm import DeclarativeMeta, Session, declarative_base
# from sqlalchemy.sql.schema import Column
# from sqlalchemy.sql.sqltypes import Integer
#
#
# def _set_up_database(
#    engine: Engine,
#    down_revision: str | None = "base",
#    up_revision: str | None = "head",
#    config_filename: str = "alembic.ini",
# ):
#    alembic_config = AlembicConfig()
#    alembic_config.set_main_option("config_file_name", config_filename)
#    _ = cast(ConfigParser, alembic_config.file_config).read(config_filename)
#
#    # Maintain the connection so Alembic does not wipe out the in-memory database
#    # when using SQLite in-memory connections
#    # https://alembic.sqlalchemy.org/en/latest/cookbook.html#sharing-a-connection-across-one-or-more-programmatic-migration-commands
#    connection: Engine._trans_ctx = engine.begin()
#    attributes = cast(dict[Any, Any], alembic_config.attributes)
#    attributes["connection"] = connection.conn
#
#    if down_revision is not None:
#        downgrade(alembic_config, down_revision, False)
#
#    if up_revision is not None:
#        upgrade(alembic_config, up_revision, False)
#
#    return connection
#
#
# def set_up_database(injector: Injector):
#    with injector.get(Session) as session:
#        # Get a connection to share so Alembic does not wipe out the in-memory database
#        # when using SQLite in-memory connections
#        if session.bind is None:
#            raise Exception(
#                "SQLAlchemy Session is not bound to an engine. This is not supported."
#            )
#
#        with _set_up_database(session.bind.engine):
#            yield
#
#
# def test__foo():
#    Base: Type[DeclarativeMeta] = declarative_base()
#
#    class TestTable(Base):
#        __tablename__ = "test"
#        id = Column(Integer, primary_key=True)
#
#    engine = create_engine("sqlite://", echo=True)
#
#    _set_up_database(engine, None)
#
