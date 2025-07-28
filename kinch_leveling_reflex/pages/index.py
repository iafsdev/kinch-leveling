import reflex as rx
from kinch_leveling_reflex.components.header import header
from kinch_leveling_reflex.views.kinch_data import kinch_data
from kinch_leveling_reflex.states.TableState import TableState
from kinch_leveling_reflex.states.HeaderState import HeaderState

@rx.page("/", title="Kinch Leveling", on_load=[TableState.load_data, HeaderState.load_data])
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        header(),
        kinch_data(),
        direction='column',
        align='center',
        spacing='3',
    )