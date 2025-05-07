"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from kinch_leveling_reflex.pages.table import table
from kinch_leveling_reflex.pages.modal import modal
from kinch_leveling_reflex.api.api import fastapi_app
from rxconfig import config
from kinch_leveling_reflex.states.TableState import TableState
from kinch_leveling_reflex.states.HeaderState import HeaderState


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        rx.container(   
            rx.heading(
            'Kinch Leveling',
            size='8',
            font_weight='bold',
            align='center',
            ),
        ),
        rx.flex(
            rx.text(f'PR Kinch: {HeaderState.pr_kinch}'),
            rx.text(f'NR Kinch: {HeaderState.nr_kinch}'),
            rx.text(f'WR Kinch: {HeaderState.wr_kinch}'),
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
app.add_page(index, on_load=[TableState.load_data, HeaderState.load_data])