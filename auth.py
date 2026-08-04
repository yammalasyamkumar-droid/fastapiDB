import jwt
from fastapi import Request, HTTPException, Depends

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"


# ==========================
# Get Current Logged-in User
# ==========================

def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# ==========================
# Verify Admin
# ==========================

def verify_admin(current_user: dict = Depends(get_current_user)):
    """
    Allows only admin users.
    """

    if current_user.get("is_admin") is not True:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user