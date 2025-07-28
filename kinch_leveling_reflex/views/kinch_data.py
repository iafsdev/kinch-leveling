import reflex as rx
from kinch_leveling_reflex.components.kinch_sum import kinch_sum
from kinch_leveling_reflex.components.table import table
from kinch_leveling_reflex.components.modal import modal

def kinch_data() -> rx.Component:
  return rx.flex(
    kinch_sum(),
    table(),
    modal(),
    direction='column',
    align='center',
    spacing='3',
    width="100%",
  )