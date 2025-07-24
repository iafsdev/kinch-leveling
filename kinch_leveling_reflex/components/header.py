import reflex as rx
from kinch_leveling_reflex.states.AuthState import AuthState

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading(
                "Kinch Leveling", size="7", weight="bold"
            ),
            rx.menu.root(
                rx.menu.trigger(
                    rx.icon_button(
                        rx.icon("user"),
                        size="2",
                        radius="full",
                    )
                ),
                rx.menu.content(
                    rx.menu.item(AuthState.wca_id),
                    rx.menu.separator(),
                    rx.menu.item(
                        rx.cond(AuthState.isLogin, "Log out", "Log in"),
                        on_click=AuthState.login
                    ),
                ),
                justify="end",
            ),
            justify="between",
            align_items="center",
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )