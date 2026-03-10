"""
IdentityService — org/workspace membership, RBAC, and SSO claim handling.

Integrates with WorkOS for SAML/OIDC enterprise SSO.
Issues JWT tokens for API access.
Enforces workspace-scoped RBAC for all resource access.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.identity_schema import (
    TokenResponse,
    UserLoginRequest,
    UserResponse,
    WorkspaceCreateRequest,
    WorkspaceResponse,
)


class IdentityService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def login(self, payload: UserLoginRequest) -> TokenResponse | None:
        """
        Authenticate a user and issue a JWT access token.

        Validates credentials (or SSO claims) and returns a signed token.
        Returns None for invalid credentials — routes convert this to 401.
        """
        raise NotImplementedError

    async def get_current_user(self) -> UserResponse:
        """
        Return the authenticated user profile from the current request context.

        Reads the JWT from the request, validates it, and fetches the user record.
        """
        raise NotImplementedError

    async def create_workspace(self, payload: WorkspaceCreateRequest) -> WorkspaceResponse:
        """Create a new workspace scoped to the authenticated org."""
        raise NotImplementedError

    async def get_workspace(self, workspace_id: str) -> WorkspaceResponse | None:
        """Return workspace details including member roles, or None if not found."""
        raise NotImplementedError

    async def check_permission(
        self, user_id: str, workspace_id: str, required_role: str
    ) -> bool:
        """
        Enforce workspace-scoped RBAC.

        Returns True if the user holds at least the required_role in the workspace.
        Used as a dependency in routes that need permission checks beyond authentication.
        """
        raise NotImplementedError
