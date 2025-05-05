import reflex as rx
from kinch_leveling_reflex.serializers import Category

def row(category: Category) -> rx.Component:
  return rx.table.row(
    rx.table.cell(category.name),
    rx.table.cell('0.00'),
    rx.table.cell('0.00'),
    rx.table.cell('0.00'),
    rx.table.cell('0.00'),
  )