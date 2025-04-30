import reflex as rx

def form() -> rx.Component:
    return rx.flex(
      rx.form(
        rx.flex(
          rx.select(
            ['SQ1', '2x2', '3x3'],
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