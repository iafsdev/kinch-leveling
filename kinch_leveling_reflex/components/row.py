import reflex as rx
from kinch_leveling_reflex.serializers import Row

def row(row: Row) -> rx.Component:
  return rx.table.row(
    rx.table.cell(row.category),
    rx.table.cell(row.pr_kinch),
    rx.table.cell(row.nr_kinch),
    rx.table.cell(row.wr_kinch),
    rx.table.cell(row.kaizen),
  )