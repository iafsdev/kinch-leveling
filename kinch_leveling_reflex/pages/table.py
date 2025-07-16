import reflex as rx
from kinch_leveling_reflex.states.TableState import TableState
from kinch_leveling_reflex.components.row import row

def table() -> rx.Component:
  return rx.table.root(
    rx.table.header(
      rx.table.row(
        rx.table.column_header_cell('Categoría'),
        rx.table.column_header_cell('PB Kinch'),
        rx.table.column_header_cell('PR Kinch'),
        rx.table.column_header_cell('NR Kinch'),
        rx.table.column_header_cell('WR Kinch'),
        rx.table.column_header_cell('Kaizen'),
        rx.table.column_header_cell('XP')
      ),
    ),
    rx.table.body(
      rx.foreach(
        TableState.rows,
        row,
      ),
    ),
    variant='surface',
    width='80%',
    align='center',
  )