# import re
# from configparser import ConfigParser
# from contextlib import \
#    _GeneratorContextManager
# from contextlib import ExitStack
# from importlib import reload
# from os import PathLike, environ
# from random import choices
# from string import ascii_letters, ascii_uppercase
# from typing import (Any, Callable, Generator, List, Optional, Protocol, Tuple,
#                    cast)
#
# import _pytest.config
# import _pytest.main
# import _pytest.python
# import pytest
# from _pytest.fixtures import SubRequest
# from connexion.apps.flask_app import FlaskApp
##from alembic.command import downgrade, upgrade
##from alembic.config import Config as AlembicConfig
##from CAP.app import create_app
##from CAP.app.models.user.role import Role as UserRole
##from CAP.app.models.user.user import User, UserId
##from CAP.database.models.CAP import *
##from CAP.database.models.CAP import Experiment
##from CAP.util.dict import merge
##from CAP.util.encryption import encrypt_flask_cookie
# from flask.sessions import SecureCookieSession
# from flask.testing import FlaskClient
# from flask.wrappers import Response
# from flask_injector import FlaskInjector
# from injector import Injector
# from pytest_mock.plugin import MockerFixture
# from sqlalchemy.engine import Engine
# from sqlalchemy.orm.session import Session
#
##from werkzeug.local import LocalProxy
#
# ClientInjector = Tuple["FlaskClient[Response]", FlaskInjector]
#
#
# def get_random_str(k=None, characters=ascii_letters):
#   if k is None:
#       k = len(characters)
#   return "".join(choices(characters, k=k))
#
#
# class FlaskAppFactory(Protocol):
#    def __call__(
#        self, name: Optional[str] = None, environment: Optional[str] = None
#    ) -> Tuple[FlaskApp, FlaskInjector]:
#        ...
#
# def _client_injector(
#   request: SubRequest, mocker: MockerFixture, app_factory: Optional[FlaskAppFactory] = None
# ) -> Generator[ClientInjector, None, None]:
#   """
#   Returns a FlaskClient[Response] and a FlaskInjector.
#   Performs all Flask CAP application initialization.
#   Performs mocking and patching of global contexts. This behavior can be changed with `pytest.mark.parametrize`.
#   The non-fixture method that gets an instance of a `ClientInjector`.
#
#   :param SubRequest request: This fixture is used to specify whether `json_logging`
#       and `login_manager` are patched for the lifetime of the test. By default, both are patched.
#       This can be changed by using the `pytest.mark.parametrize` decorator on a test.
#       For example, pass sequence of an array of two bools. To prevent patching of both modules,
#       use `[False, False, [], False]`. The first bool is for `json_logging`, and the second is for `login_manager`.
#       The third item is a list of user roles for a mocked user object to hold. This mocked user object is
#       used as part of patching login_manager, and only applies if `patch_login_manager` is true. By default,
#       this user object holds the "Role.Staff" role. The forth bool determines whether to patch the Flask app config
#       with default values.
#
#       ```
#       import pytest
#       @pytest.mark.parametrize('client_injector', [[True, True, [Role.Staff], True]], indirect=['client_injector'])
#       def test_foo(client_injector: ClientInjector): ...
#       ```
#   """
#
#   #patch_json_logging = True
#   #patch_login_manager = True
#   #patch_user_roles = [UserRole.Staff]
#   #force_config_values = True
#   #if hasattr(request, "param"):
#   #    (
#   #        patch_json_logging,
#   #        patch_login_manager,
#   #        patch_user_roles,
#   #        force_config_values,
#   #    ) = cast(Tuple[bool, bool, List[UserRole], bool], request.param)
#   patch_json_logging = True
#   patch_login_manager = True
#   force_config_values = True
#   if hasattr(request, "param"):
#       (
#           patch_json_logging,
#           patch_login_manager,
#           force_config_values,
#       ) = cast(Tuple[bool, bool, bool], request.param)
#
#   if patch_json_logging:
#       mocker.patch("json_logging.init_connexion")
#
#       mocker.patch("json_logging.init_request_instrument")
#
#   #mock_username = "abc xyz"
#   #if patch_login_manager:
#   #    assert isinstance(patch_user_roles, list) and all(
#   #        [isinstance(role, UserRole) for role in patch_user_roles]
#   #    ), "All patched user roles must be of type Role."
#
#   #    def get_mock_user(proxy: LocalProxy = None):
#   #        if proxy is not None:
#   #            return proxy
#   #        user_id = UserId(1, mock_username)
#   #        return User(user_id, patch_user_roles)
#
#   #    mocker.patch("flask_login.utils._get_user", side_effect=get_mock_user)
#
#   environ.setdefault("OPENAPI_SPEC_DIR", "swagger/")
#   # if not app_factory then use create_app
#   connexion_app, flask_injector = app_factory(environment="test")
#
#   app = connexion_app.app
#   app.testing = True
#
#   if force_config_values:
#       # add any required but missing config keys, without overwriting
#       merge(
#           app.config,
#           {
#               "DATABASE_CONNECTION_STRING": "sqlite:///:memory:",
#               "SAML2_METADATA_URL": "http://example.edu/saml2",
#               "SAML2_RELAY_STATE": "http://example.edu",
#               "SAML2_LOGGING": {},
#           },
#           True,
#       )
#
#       # force overwriting of key test config parameters
#       # fmt: off
#       merge(
#           app.config,
#           {
#               "ENV": "test",
#               "DEBUG": True,
#               "SECRET_KEY": get_random_str(),
#            },
#           False,
#       )
#       # fmt: on
#   else:
#       # otherwise, these configuration variables are required,
#       # so we set them if they are not already set
#       # fmt: off
#       merge(
#           app.config,
#           {
#               "ENV": "test",
#               "DEBUG": True,
#               "SECRET_KEY": get_random_str(),
#           },
#           True,
#       )
#       # fmt: on
#
#   with ExitStack() as stack:
#       client = app.test_client()
#       flask_session_ctx_manager = cast(
#           _GeneratorContextManager[SecureCookieSession], client.session_transaction()
#       )
#
#       stack.enter_context(app.test_client())
#       flask_session = stack.enter_context(flask_session_ctx_manager)
#       flask_session["_id"] = get_random_str()
#
#       if patch_login_manager:
#           flask_session["authenticated"] = True
#           flask_session["username"] = mock_username
#
#       client.set_cookie(
#           "localhost",
#           app.session_cookie_name,
#           encrypt_flask_cookie(app.config["SECRET_KEY"], flask_session),
#           # fmt: off
#           max_age=app.config['PERMANENT_SESSION_LIFETIME'] if app.config['PERMANENT_SESSION'] else None,
#           # fmt: on
#       )
#
#       yield (client, flask_injector)
#
#
