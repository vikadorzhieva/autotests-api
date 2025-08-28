import pytest
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from clients.users.public_users_client import get_public_users_client, PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema



class UserFixture(BaseModel):
    """
    Модель-контейнер для агрегации данных тестового пользователя.
    
    Объединяет все связанные данные пользователя в одном объекте для удобства
    использования в тестах. Содержит исходный запрос, ответ API и данные для аутентификации.
    
    Attributes:
        request: Исходный запрос на создание пользователя со сгенерированными данными.
        response: Ответ API после успешного создания пользователя.
        authentication_user: Данные для аутентификации (email и password).
    """
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema
    authentication_user: AuthenticationUserSchema

    @property
    def email(self) -> EmailStr:
        """Быстрый доступ к email пользователя из запроса."""
        return self.request.email

    @property
    def password(self) -> str:
        """Быстрый доступ к password пользователя из запроса."""
        return self.request.password


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    """
    Фикстура для получения клиента аутентификации.
    
    Создает и возвращает экземпляр клиента для работы с API аутентификации.
    Не требует предварительной настройки или аутентификации.
    
    :return: AuthenticationClient для работы с endpoints аутентификации.
    """
    return get_authentication_client()


@pytest.fixture
def public_users_client() -> PublicUsersClient:
    """
    Фикстура для получения клиента публичного API пользователей.
    
    Создает и возвращает экземпляр клиента для работы с публичными endpoints
    API пользователей. Не требует аутентификации.

    :return: PublicUsersClient для работы с публичными endpoints пользователей.
    """
    return get_public_users_client()


@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    """
    Фикстура для создания тестового пользователя с данными для аутентификации.
    
    Создает нового пользователя через Public API, генерирует случайные данные
    и возвращает агрегированный объект со всеми необходимыми данными.
    
    :param public_users_client: Фикстура клиента для публичного API пользователей.
    :return: UserFixture с данными созданного пользователя:
        - request: Исходный запрос на создание
        - response: Ответ от API с данными пользователя  
        - authentication_user: Данные для аутентификации (email/password)
    :raises AssertionError: Если создание пользователя не удалось.
    """
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    authentication_user = AuthenticationUserSchema(
        email=request.email,
        password=request.password
    )
    return UserFixture(request=request, response=response, authentication_user=authentication_user)


@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    """
    Фикстура для создания аутентифицированного клиента приватного API пользователей.
    
    Создает и возвращает API-клиент с предустановленной аутентификацией
    используя данные созданного тестового пользователя.
    
    :param function_user: Фикстура с данными тестового пользователя.
    :return: PrivateUsersClient с настроенной аутентификацией.
    """
    return get_private_users_client(function_user.authentication_user)
