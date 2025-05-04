"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from kinch_leveling_reflex.components.table import table
from kinch_leveling_reflex.components.modal import modal
from kinch_leveling_reflex.api.api import fastapi_app
from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        rx.container(   
            rx.heading(
            'Kinch',
            size='8',
            font_weight='bold',
            align='center',
            ),
        ),
        rx.flex(
            rx.text('PR Kinch: 0.00'),
            rx.text('NR Kinch: 0.00'),
            rx.text('WR Kinch: 0.00'),
            justify='center',
            spacing='9',
        ),
        table(),
        modal(),
        direction='column',
        align='center',
        spacing='3',
    )

app = rx.App(
    api_transformer=fastapi_app,
)
app.add_page(index)