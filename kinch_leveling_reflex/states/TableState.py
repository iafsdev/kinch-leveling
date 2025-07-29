import reflex as rx
from kinch_leveling_reflex.api.api import get_categories, get_kaizen, get_pbs, get_pr_kinch, get_wca_events
from kinch_leveling_reflex.serializers import Category, Row, Record
from kinch_leveling_reflex.states.WCAState import WCAState
from kinch_leveling_reflex.states.AuthState import AuthState

class TableState(rx.State):
  categories: list[Category]    
  kaizen: dict[str, str]
  rows: list[Row]
  pbs: dict[str, float]
  xp: dict[str, int]
  prs: dict[str, float]
  nrs: dict[str, float]
  wrs: dict[str, float]
  wca_categories: list[Record]
  wca_id: str
  
  @rx.event
  async def load_data(self):
    wca_state = await self.get_state(WCAState)
    self.wca_categories = wca_state.wca_categories
    auth_state = await self.get_state(AuthState)
    self.wca_id = auth_state.wca_id

    self.categories = await get_categories()
    self.kaizen = await get_kaizen(self.wca_id)
    self.pbs, self.xp = await get_pbs(self.wca_id)
    self.prs = await get_pr_kinch(self.wca_categories, self.wca_id)
    self.nrs = await wca_state.nr_kinch
    self.wrs = await wca_state.wr_kinch
    self.rows = []
    if self.wca_id:
      for category in self.categories:
        self.rows.append(Row(
          category=category.name,
          pb_kinch=self.pbs[category.name],
          pr_kinch=self.prs[category.name],
          nr_kinch=self.nrs[category.name],
          wr_kinch=self.wrs[category.name],
          kaizen=self.kaizen[category.name],
          xp=self.xp[category.name]
        ))
