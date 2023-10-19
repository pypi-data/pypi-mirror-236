import enum


class GrantType(enum.StrEnum):
    """인증 방식"""

    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"


class Token:
    """토큰 정보"""

    def __init__(
        self,
        access_token,
        expires_in,
        token_type,
        scope,
        refresh_token=None,
        id_token=None,
    ):
        # 토큰 정보
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.scope = scope
        self.id_token = id_token


class Resource:
    """리소스"""

    def __init__(self, user_id, millie_id=None, profile=None):
        self.user_id = user_id
        # 사용자 정보
        self.millie_id = millie_id
        self.profile = profile


class Connect:
    """사용자 연동"""

    def __init__(
        self,
        is_connected: bool,
        created_at: str = None,
        error: dict = None
    ):
        self.is_connected = is_connected
        self.created_at = created_at
        self.error = error

    class Validate:
        """사용자 연동 전 유효성 검사"""

        def __init__(
            self,
            is_valid: bool,
            validate_key: str = None,
            created_at: str = None,
            error: dict = None
        ):
            self.is_valid = is_valid
            self.validate_key = validate_key
            self.created_at = created_at
            self.error = error


class Disconnect:
    """사용자 연동 끊기"""

    def __init__(
        self,
        is_connected: bool = None,
        external_id: int = None,
        external_service: str = None,
        error: dict = None
    ):
        self.is_connected = is_connected
        self.external_id = external_id
        self.external_service = external_service
        self.error = error
