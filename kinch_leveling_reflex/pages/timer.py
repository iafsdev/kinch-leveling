import reflex as rx
from kinch_leveling_reflex.hooks.SpacebarUpWatcher import SpacebarUpWatcher
from kinch_leveling_reflex.hooks.SpacebarDownWatcher import SpacebarDownWatcher
from kinch_leveling_reflex.states.TimerState import TimerState

@rx.page('/timer', title='Timer Example', on_load=TimerState.increment)
def timer() -> rx.Component:
  return rx.box(
    SpacebarUpWatcher.create(
      on_space=TimerState.toggle_timer(action="up")
    ),
    SpacebarDownWatcher.create(
      on_space=TimerState.toggle_timer(action="down")
    ),
    rx.heading(TimerState.formatted_time, size='8')
  )