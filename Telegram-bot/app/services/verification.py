from .database import get_user

async def verify_user(user_id: int) -> bool:
    """Verify if a user is registered."""
    user = get_user(user_id)
    return user is not None