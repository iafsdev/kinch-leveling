import reflex as rx
from .form import form
from kinch_leveling_reflex.states.FormState import FormState

def modal() -> rx.Component:
  return rx.dialog.root(
    rx.dialog.trigger(rx.button('Editar', on_click=FormState.fetch_categories)),
    rx.dialog.content(
      rx.flex(
        rx.dialog.title(
          'Editar Tiempos',
        ),
        form(),
        rx.flex(
          rx.dialog.close(
            rx.button('Guardar'),
          ),
          justify='center',
        ),
        direction='column',
        spacing='3',
      )
    )
  ),