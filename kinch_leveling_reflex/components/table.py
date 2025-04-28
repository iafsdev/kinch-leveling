import reflex as rx

def table() -> rx.Component:
  return rx.table.root(
    rx.table.header(
      rx.table.row(
        rx.table.column_header_cell('Categoría'),
        rx.table.column_header_cell('PR Kinch'),
        rx.table.column_header_cell('NR Kinch'),
        rx.table.column_header_cell('WR Kinch'),
        rx.table.column_header_cell('Kaizen'),
      ),
    ),
    rx.table.body(
      rx.table.row(
        rx.table.cell('SQ1'),
        rx.table.cell('0.00'),
        rx.table.cell('0.00'),
        rx.table.cell('0.00'),
        rx.table.cell('0.00'),
      ),
    ),
    variant='surface',
    width='80%',
    align='center',
  )