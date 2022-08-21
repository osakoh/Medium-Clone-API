# noinspection PyUnresolvedReferences
import pytest


def test_user_str(base_user):
    """
    Test the string representation in the custom user class
    base_user: passes as a parameter. It's defined in the "conftest.py" script
    """
    # the str repr defined in the custom user model is "self.username"
    assert base_user.__str__() == f"{base_user.username}"


def test_user_short_name(base_user):
    """
    Test the "get_short_name()" method in the custom user class
    base_user: passes as a parameter. It's defined in the "conftest.py" script
    """

    print(f"\n************************* In core.test_models.test_user_short_name *****************************")
    print(f"base_user.get_short_name(): {base_user.get_short_name()}")
    print(f"short_name: {base_user.first_name}")
    print(f"************************* In core.test_models.test_user_short_name *****************************\n")

    short_name = f"{base_user.first_name}"
    assert base_user.get_short_name() == short_name


def test_user_full_name(base_user):
    """
    Test the "get_full_name()" method in the custom user class
    base_user: passes as a parameter. It's defined in the "conftest.py" script
    """

    print(f"\n************************* In core.test_models.test_user_full_name *****************************")
    print(f"base_user.get_full_name: {base_user.get_full_name}")
    print(f"************************* In core.test_models.test_user_full_name *****************************\n")

    full_name = f"{base_user.first_name.title()} {base_user.last_name.title()}"
    assert base_user.get_full_name == full_name


def test_base_user_email_is_normalized(base_user):
    """
    Test the normal users' Email is normalized in the custom user class
    base_user: passes as a parameter. It's defined in the "conftest.py" script
    """
    email = base_user.email
    assert email == email.lower()


def test_super_user_email_is_normalized(super_user):
    """
    Test the super_users' Email is normalized in the custom user class
    base_user: passes as a parameter. It's defined in the "conftest.py" script
    """
    email = super_user.email
    assert email == email.lower()


def test_super_user_is_not_staff(user_factory):
    """
    Test that a ValueError is raised if an attempt is made to create a superuser without setting is_staff to True
    """
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)

    print(f"\n******************** In core.test_models.test_super_user_is_not_staff ***********************")
    print(f"err: {err}")
    print(f"user_factory: {user_factory}")
    print(f"err.value: {err.value}")
    print(f"******************** In core.test_models.test_super_user_is_not_staff *********************\n")

    assert str(err.value) == "Superuser must be a staff"


def test_super_user_is_not_superuser(user_factory):
    """
    Test that a ValueError is raised if an attempt is made to create a superuser without setting is_superuser to True
    """
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)

    print(f"\n******************** In core.test_models.test_super_user_is_not_staff ***********************")
    print(f"err: {err}")
    print(f"user_factory: {user_factory}")
    print(f"err.value: {err.value}")
    print(f"******************** In core.test_models.test_super_user_is_not_staff *********************\n")

    assert str(err.value) == "Superuser must set to True"


def test_create_user_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "Email address must be provided"


def test_create_user_with_no_username(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None)
    assert str(err.value) == "Username must be provided"


def test_create_user_with_no_firstname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "First name must be provided"


def test_create_user_with_no_lastname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "Last name must be provided"


def test_create_superuser_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Email address must be provided for an Admin"


def test_create_superuser_with_no_password(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Superusers must have a password"


def test_user_email_incorrect(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email="test.com")
    assert str(err.value) == "Email is invalid"


@pytest.mark.skip(reason="Not yet implemented-BaseUser")
def test_base_user_username_spaces_punctuations_are_removed(base_user):
    """
    Test all spaces/punctuations are removed when a users' username is created
                # remove all spaces/comma/punctuations
            self.username = "".join(re.findall(r"\w", self.username.lower()))
    """
    pass
