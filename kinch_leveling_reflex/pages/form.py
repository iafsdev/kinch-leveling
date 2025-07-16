import reflex as rx
from kinch_leveling_reflex.states.FormState import FormState
from kinch_leveling_reflex.states.TableState import TableState
from kinch_leveling_reflex.states.HeaderState import HeaderState

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
          rx.input(placeholder='Tiempo actual', value=FormState.actual_time, on_change=FormState.set_actual_time),
          rx.input(placeholder='Tiempo objetivo', value=FormState.goal_time, on_change=FormState.set_goal_time),
          rx.select(
            ['Nula', 'Baja', 'Media', 'Alta'],
            width='100%',
            placeholder='Seleccionar cantidad de mejora',
            value=FormState.proportion,
            on_change=FormState.set_proportion,
          ),
          rx.flex(
            rx.dialog.close(
              rx.button(
                'Guardar',
                type='submit',
                on_click=[FormState.update_category_time(TableState.kaizen, TableState.xp), TableState.load_data, HeaderState.load_data],
              ),
            ),
            justify='center',
          ),
          direction='column',
          spacing='2',
        ),
      )
    )