import reflex as rx
from kinch_leveling_reflex.components.header import header
from kinch_leveling_reflex.views.kinch_data import kinch_data
from kinch_leveling_reflex.states.TableState import TableState
from kinch_leveling_reflex.states.HeaderState import HeaderState
from kinch_leveling_reflex.states.AuthState import AuthState

@rx.page("/", title="Kinch Leveling", on_load=[TableState.load_data, HeaderState.load_data])
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        header(),
        rx.cond(
            AuthState.isLogin,
            kinch_data(),
            rx.center(
                rx.text(
                    'Login with your WCA account',
                    size='7',
                    weight='bold',
                ),
                justify='center',
                align='center',
                height='90vh',
            )
        ),
        direction='column',
        align='center',
        spacing='3',
    )