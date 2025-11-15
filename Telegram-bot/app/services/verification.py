from .database import get_user, update_user_verification

async def verify_user(user_id: int) -> bool:
    """Verify if a user is registered."""
    user = get_user(user_id)
    return user is not None

async def is_user_verified(user_id: int) -> bool:
    """Check if a user is verified."""
    user = get_user(user_id)
    return user is not None and user.is_verified

async def verify_user_account(user_id: int) -> bool:
    """Verify a user account (admin function)."""
    return update_user_verification(user_id, True)

async def unverify_user_account(user_id: int) -> bool:
    """Unverify a user account (admin function)."""
    return update_user_verification(user_id, False)