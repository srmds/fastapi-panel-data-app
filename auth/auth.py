import os
from fastapi_login import LoginManager
from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("console.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
security = HTTPBasic()

try:
    secret = os.getenv("SECRET", os.urandom(24).hex())
except KeyError as e:
    raise Exception(f"Could not find env var: {e}, make sure to export it")

manager = LoginManager(secret, token_url='/auth/token', use_cookie=True)
user = os.getenv("USER", "johndoe@e.mail")
password = os.getenv("PASS", os.urandom(24).hex())

fake_db = {user: {'password': password}}


@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user


class NotAuthenticatedException(Exception):
    pass


# these two argument are mandatory
def exc_handler(request, exc):
    return RedirectResponse(url='/login')


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = next(iter(fake_db))
    passw = list(fake_db.values())[0]
    passw = list(passw.values())[0]
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, passw)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    logger.info(f"CRED {credentials}")

    return False
