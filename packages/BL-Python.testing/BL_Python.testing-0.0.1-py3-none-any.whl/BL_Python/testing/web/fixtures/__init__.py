# from typing import Callable, Optional, Protocol, Tuple
#
# import pytest
# from _pytest.fixtures import SubRequest
# from connexion.apps.flask_app import FlaskApp
# from flask_injector import FlaskInjector
# from pytest_mock.plugin import MockerFixture
#
# from .. import _client_injector
# from .. import ClientInjector, FlaskAppFactory
#
#
# @pytest.fixture
# def client_injector(request: SubRequest, mocker: MockerFixture) -> ClientInjector:
#    """
#    Get an instance of a `FlaskInjector` from the `flask_injector` fixture.
#    """
#    return next(_client_injector(request, mocker))
#
#
# @pytest.fixture
# def client_injector_factory(
#    request: SubRequest, mocker: MockerFixture
# ) -> Callable[[FlaskAppFactory], ClientInjector]:
#    """
#    This fixture returns a method that can be used to get an
#    instance of the same type that the `client_injector` fixture would return.
#    """
#    return lambda app_factory: next(_client_injector(request, mocker, app_factory))
#
