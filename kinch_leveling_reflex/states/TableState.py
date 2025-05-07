import reflex as rx
from kinch_leveling_reflex.api.api import get_categories, get_kaizen, get_prs, get_nr_kinch, get_wr_kinch
from kinch_leveling_reflex.serializers import Category, Row

class TableState(rx.State):
  categories: list[Category]    
  kaizen: dict[str, str]
  rows: list[Row]
  prs: dict[str, float]
  nrs: dict[str, float]
  wrs: dict[str, float]
  
  @rx.event
  async def load_data(self):
    self.categories = await get_categories()
    self.kaizen = await get_kaizen()
    self.prs = await get_prs()
    self.nrs = await get_nr_kinch()
    self.wrs = await get_wr_kinch()
    self.rows = []
    for category in self.categories:
      self.rows.append(Row(
        category=category.name,
        pr_kinch=self.prs[category.name],
        nr_kinch=self.nrs[category.name],
        wr_kinch=self.wrs[category.name],
        kaizen=self.kaizen[category.name],
      ))
