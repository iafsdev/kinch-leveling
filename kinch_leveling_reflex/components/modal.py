import reflex as rx

def modal() -> rx.Component:
  return rx.dialog.root(
    rx.dialog.trigger(rx.button('Editar')),
    rx.dialog.content(
      rx.dialog.title(
        'Editar Tiempos',
      ),
      align='center'
    )
  ),