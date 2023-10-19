# from typing import Any, Callable, Union
#
# from alembic.command import downgrade, upgrade
# from alembic.config import Config as AlembicConfig
# from injector import Binder, CallableProvider, Module, inject, singleton
# from sqlalchemy import create_engine, event
# from sqlalchemy.engine import Engine
# from sqlalchemy.orm.scoping import ScopedSession
# from sqlalchemy.orm.session import Session, sessionmaker
#
#
# class SQLiteScopedSession(ScopedSession):
#    @staticmethod
#    def create(connection_string: str, echo: bool = False):
#        """
#        Create a new session factory for SQLite.
#        """
#        engine = create_engine(
#            connection_string,
#            echo=echo,
#        )
#
#        return SQLiteScopedSession(
#            sessionmaker(autocommit=False, autoflush=False, bind=engine)
#        )
#
#    def __init__(
#        self,
#        session_factory: Union[Callable[..., Any], "sessionmaker[Any]"],
#        scopefunc: Any = None,
#    ) -> None:
#        super().__init__(session_factory, scopefunc)
#        """
#        This callback is used to subscribe to the "connect" core SQLAlchemy event.
#        When a session is instantiated from sessionmaker, and immediately after a connection
#        is made to the database, this will issue the `pragma foreign_key=ON` query. This
#        query ensures SQLite respects foreign key constraints.
#        This will be removed at a later date.
#        """
#
#        def _fk_pragma_on_connect(dbapi_con: Any, con_record: Any):
#            """
#            Called immediately after a connection is established.
#            """
#            dbapi_con.execute("pragma foreign_keys=ON")
#
#        event.listen(self.bind, "connect", _fk_pragma_on_connect)
#
#
# class ScopedSessionModule(Module):
#    """
#    Configure SQLAlchemy Session depedencies for Injector.
#    """
#
#    def __init__(self, connection_string: str, sqlalchemy_echo: bool = False):
#        assert (
#            connection_string is not None
#        ), "Cannot initialize the database module without a valid connection string"
#        super().__init__()
#        self._connection_string = connection_string
#        self._sqlalchemy_echo = sqlalchemy_echo
#
#    def configure(self, binder: Binder) -> None:
#        # Any ScopedSession dependency should be the same for the lifetime of the application.
#        # ScopeSession is a factory that creates a Session per thread.
#        # The Session returned is the same for the lifetime of the thread.
#        binder.bind(
#            ScopedSession,
#            to=CallableProvider(self._get_scoped_session),
#            scope=singleton,
#        )
#
#        # Injecting a Session means calling the ScopedSession factory.
#        # This is largely a convenience dependency, because the same
#        # instance can be obtained by executing the factory that is
#        # ScopedSession. ScopedSession handles all thread local concerns.
#        # It is safe for this method to be called multiple times.
#        binder.bind(Session, to=CallableProvider(self._get_session))
#
#    @inject
#    def _get_scoped_session(self) -> ScopedSession:
#        """
#        Returns a ScopedSession instance configured with
#        the correct engine and connection string.
#        Defaults to using the `sessionmaker` Session factory.
#        """
#        return SQLiteScopedSession.create(
#            self._connection_string, self._sqlalchemy_echo
#        )
#
#    @inject
#    def _get_session(self, session_factory: ScopedSession) -> Session:
#        """
#        Returns a Session instance from the injected ScopedSession instance.
#        """
#        session: Session = session_factory()
#        return session
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
#    alembic_config.file_config.read(config_filename)
#
#    # Maintain the connection so Alembic does not wipe out the in-memory database
#    # when using SQLite in-memory connections
#    # https://alembic.sqlalchemy.org/en/latest/cookbook.html#sharing-a-connection-across-one-or-more-programmatic-migration-commands
#    connection = engine.begin()
#    alembic_config.attributes["connection"] = connection.conn
#
#    if down_revision is not None:
#        downgrade(alembic_config, down_revision, False)
#
#    if up_revision is not None:
#        upgrade(alembic_config, up_revision, False)
#
#    return connection
#
