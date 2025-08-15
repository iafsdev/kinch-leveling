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
      value=TimerState.category,
      on_change=TimerState.get_scramble
    ),
    rx.heading(TimerState.formatted_time, size='9'),
    rx.text(
      TimerState.scramble,
      width='80%',
      align='center',
    ),
    rx.center(
      rx.html(TimerState.svg_scramble, width='100%', height='100%'),
      height='20vh',
      width='20vh'
    ),
    direction='column',
    align_items='center',
    justify_content='center',
    height='100vh',
    spacing='5'
  )