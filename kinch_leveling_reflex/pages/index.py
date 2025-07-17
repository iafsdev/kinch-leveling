import reflex as rx
from kinch_leveling_reflex.components.header import header
from kinch_leveling_reflex.components.table import table
from kinch_leveling_reflex.components.modal import modal
from kinch_leveling_reflex.states.TableState import TableState
from kinch_leveling_reflex.states.HeaderState import HeaderState

@rx.page("/", title="Kinch Leveling", on_load=[TableState.load_data, HeaderState.load_data])
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        header(),
        rx.flex(
            rx.text(f'PB Kinch: {HeaderState.pb_kinch}'),
            rx.text(f'PR Kinch: {HeaderState.pr_kinch}'),
            rx.text(f'NR Kinch: {HeaderState.nr_kinch}'),
            rx.text(f'WR Kinch: {HeaderState.wr_kinch}'),
            rx.text(f'XP: {HeaderState.xp_total}'),
            justify='center',
            spacing='9',
        ),
        table(),
        modal(),
        direction='column',
        align='center',
        spacing='3',
    )