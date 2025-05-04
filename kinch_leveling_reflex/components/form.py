import reflex as rx
from kinch_leveling_reflex.states.FormState import FormState

def form() -> rx.Component:
    return rx.flex(
      rx.form(
        rx.flex(
          rx.select(
            FormState.categories,
            width='100%',
            placeholder='Seleccionar categoría',
          ),
          rx.input(placeholder='Avg100'),
          rx.input(placeholder='Avg1000'),
          rx.select(
            ['Nula', 'Baja', 'Media', 'Alta'],
            width='100%',
            placeholder='Seleccionar cantidad de mejora',
          ),
          direction='column',
          spacing='2',
        )
      )
    )