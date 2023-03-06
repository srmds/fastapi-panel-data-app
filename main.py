import panel as pn
from bokeh.embed import server_document
from fastapi import FastAPI, Request, Response, Depends
from fastapi.templating import Jinja2Templates
from auth.auth import manager, load_user, NotAuthenticatedException, exc_handler, get_current_username, authorize
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sinewave.pn_app import sinewave
from maps.pn_app import maps
from logging.config import dictConfig
import logging
from log_config import LogConfig

templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
dictConfig(LogConfig().dict())
logger = logging.getLogger(__name__)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


app = FastAPI()
configure_static(app)
app.add_exception_handler(NotAuthenticatedException, exc_handler)


@app.get("/")
async def index(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Simple sine wave example page
    """

    return templates.TemplateResponse("index.html", {"request": request, "script": None})


# @app.get("/maps")
# async def maps_app(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
#     """
#     Simple Google Maps example
#     """
#     logger.info(f"process REQQQQQQ: {request}, {get_current_username()}")
#
#     script = server_document('http://127.0.0.1:5000/maps')
#     return templates.TemplateResponse("maps.html", {"request": request, "script": script})


@app.get("/sine")
async def sine_wave_app(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Simple sine wave example page
    """
    script = server_document('http://127.0.0.1:5000/sine')
    return templates.TemplateResponse("sinewave.html", {"request": request, "script": script})


# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/auth')
def auth(response: Response, user=Depends(manager)):
    token = manager.create_access_token(
        data=dict(sub=user.email)
    )
    manager.set_cookie(response, token)

    return response

# See docs to enable authentication: https://panel.holoviz.org/user_guide/Authentication.html
# pn.config.authorize_callback = authorize

pn.serve(
    {
        '/maps': maps,
        '/sine': sinewave
    },
    port=5000,
    allow_websocket_origin=["127.0.0.1:5000"],
    address="127.0.0.1",
    show=False
)
