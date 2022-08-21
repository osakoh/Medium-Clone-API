"""
https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files#34520971
https://docs.pytest.org/en/6.2.x/writing_plugins.html
https://pytest.org/en/latest/how-to/plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file
____________________________________________________________________________________________________________
Fixtures: Define fixtures for static data used by tests. This data can be accessed by all tests in the suite unless specified otherwise. This could be data as well as helpers of modules which will be passed to all tests.

External plugin loading: conftest.py is used to import external plugins or modules.
By defining the following global variable, pytest will load the module and make it available for its test.
Plugins are generally files defined in your project or other modules which might be needed in your tests.
You can also load a set of predefined plugins as explained here.

pytest_plugins = "someapp.someplugin"

Hooks: You can specify hooks such as setup and teardown methods and much more to improve your tests.
For a set of available hooks, read Hooks link. Example:

  def pytest_runtest_setup(item):
       # called before ``pytest_runtest_call(item)
       #do some stuff`

Test root path: This is a bit of a hidden feature. By defining conftest.py in your root path,
you will have pytest recognizing your application modules without specifying PYTHONPATH.
In the background, py.test modifies your sys.path by including all submodules which are found from the root path
"""
import pytest
from pytest_factoryboy import register

# from main_apps.profiles.tests.factories import ProfileFactory
from main_apps.core.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def base_user(db, user_factory):
    """
    Normal user
    UserFactory => user_factory. i.e. lowercase-underscore class name
    """
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    """
    Superuser
    UserFactory => user_factory. i.e. lowercase-underscore class name
    """
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user
