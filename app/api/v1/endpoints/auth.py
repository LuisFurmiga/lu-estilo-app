# lu-estilo-app/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.services.user_service import create_user, get_user_by_email
from app.db.session import SessionLocal

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2 scheme
oauth2_scheme = HTTPBearer()
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return current_user

@router.post(
    "/register",
    summary="Registro de novo usuário",
    description="Cria um novo usuário com nome, email e senha.",
    response_model=UserRead
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email já registrado")
        return create_user(db, user)
    except Exception as e:
        print("Erro no registro:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@router.post(
    "/login",
    summary="Autenticação de usuário",
    description="Realiza o login do usuário com email e senha. Retorna um token JWT para ser utilizado nos endpoints autenticados."
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token_data = {
        "sub": db_user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post(
    "/refresh-token",
    summary="Renovar token JWT",
    description="Gera um novo token de acesso com base no token atual (JWT Bearer) válido. "
    "Esse endpoint é útil para manter a sessão ativa sem que o usuário precise realizar login novamente."
)
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        new_payload = {
            "sub": email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        new_token = jwt.encode(new_payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": new_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
