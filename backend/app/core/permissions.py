from typing import List
from fastapi import Depends, HTTPException, status
from app.core.security import get_current_active_user
from app.models.user import User

def require_roles(allowed_roles: List[str]):
    """
    Dependency generator for Role-Based Access Control (RBAC).
    Checks whether the current active user's role is inside allowed_roles.
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden. Required roles: {', '.join(allowed_roles)}. Your role: {current_user.role}"
            )
        return current_user
    return role_checker
