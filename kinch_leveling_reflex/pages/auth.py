import reflex as rx
from kinch_leveling_reflex.states.AuthState import AuthState

@rx.page("/auth", on_load=[AuthState.callback])
def auth() -> rx.Component:
  return rx.box()