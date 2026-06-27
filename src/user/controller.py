from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, status, Request,BackgroundTasks
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
from src.utils.mail import send_email

password_hash = PasswordHash.recommended()
EXP_TIME = 40


def get_password_hash(password: str):
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


async def register(body: UserSchema,bg_task:BackgroundTasks ,db: Session):
    # Check username
    is_user = (
        db.query(UserModel)
        .filter(UserModel.username == body.username)
        .first()
    )

    if is_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    # Check email
    is_user = (
        db.query(UserModel)
        .filter(UserModel.email == body.email)
        .first()
    )

    if is_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Send confirmation email
        # await send_email([new_user.email])
        bg_task.add_task(send_email,[new_user.email])
        return new_user

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


def login_user(body: LoginSchema, db: Session):
    user = (
        db.query(UserModel)
        .filter(UserModel.username == body.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    exp_time = datetime.utcnow() + timedelta(minutes=EXP_TIME)

    token = jwt.encode(
        {
            "_id": user.id,
            "exp": exp_time,
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


def is_authenticated(request: Request, db: Session):
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
            )

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header",
            )

        token = parts[1]

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = data.get("_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        user = (
            db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_all_users(db: Session):
    return db.query(UserModel).all()