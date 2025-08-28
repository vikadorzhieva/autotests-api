from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema
from tools.assertions.base import assert_equal


def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Сравнивает два объекта UserSchema на идентичность полей.
    
    Проверяет совпадение: id, email, last_name, first_name, middle_name.
    
    :param actual: Фактические данные пользователя (из ответа API).
    :param expected: Ожидаемые данные пользователя (эталонные).
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")

def assert_get_user_response(get_user_response, create_user_response):
    """
    Проверяет, что данные пользователя при запросе совпадают с данными при создании.
    
    Сравнивает объекты UserSchema из ответа на GET-запрос пользователя 
    и из ответа на создание пользователя.
    
    :param get_user_response: Данные пользователя из ответа GET /api/v1/users/me.
    :param create_user_response: Данные пользователя из ответа на создание пользователя.
    :raises AssertionError: Если данные пользователя не совпадают.
    """
    assert_user(get_user_response, create_user_response)
