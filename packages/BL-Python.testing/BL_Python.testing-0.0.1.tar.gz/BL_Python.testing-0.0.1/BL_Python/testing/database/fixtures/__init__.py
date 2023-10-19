# import pytest
# from injector import Injector
# from sqlalchemy.orm import Session
#
# from .. import _set_up_database
# from .. import ScopedSessionModule
#
#
# @pytest.fixture
# def injector():
#    return Injector(ScopedSessionModule("sqlite:///:memory:", True))
#
#
# @pytest.fixture
# def session(injector: Injector):  # , set_up_database) -> Session:
#    return injector.get(Session)
#
#
# @pytest.fixture
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
