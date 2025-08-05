import reflex as rx
from kinch_leveling_reflex.pages.index import index
from kinch_leveling_reflex.pages.auth import auth
from kinch_leveling_reflex.pages.timer import timer
from kinch_leveling_reflex.api.api import fastapi_app
from rxconfig import config

app = rx.App(
    api_transformer=fastapi_app,
    theme=rx.theme(
        appearance="dark",
        accent_color="iris"
    )
)