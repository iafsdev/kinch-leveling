import reflex as rx
from kinch_leveling_reflex.hooks.SpacebarUpWatcher import SpacebarUpWatcher
from kinch_leveling_reflex.hooks.SpacebarDownWatcher import SpacebarDownWatcher
from kinch_leveling_reflex.states.TimerState import TimerState

@rx.page('/timer', title='Timer Example', on_load=TimerState.increment)
def timer() -> rx.Component:
  return rx.flex(
    SpacebarUpWatcher.create(
      on_space=TimerState.toggle_timer(action="up")
    ),
    SpacebarDownWatcher.create(
      on_space=TimerState.toggle_timer(action="down")
    ),
    rx.select(
      TimerState.categories,
      width='20%',
      placeholder='Seleccionar categoría',
      on_change=TimerState.get_scramble
    ),
    rx.heading(TimerState.formatted_time, size='9'),
    rx.text(TimerState.scramble),
    # rx.image(src='/scramble.svg'),
    direction='column',
    align_items='center',
    justify_content='center',
    height='100vh',
    spacing='5'
  )