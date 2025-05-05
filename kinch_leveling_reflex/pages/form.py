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
            on_change=FormState.get_category_times
          ),
          rx.input(placeholder='Avg100', value=FormState.actual_time),
          rx.input(placeholder='Avg1000', value=FormState.goal_time),
          rx.select(
            ['Nula', 'Baja', 'Media', 'Alta'],
            width='100%',
            placeholder='Seleccionar cantidad de mejora',
            value=FormState.proportion,
          ),
          direction='column',
          spacing='2',
        )
      )
    )