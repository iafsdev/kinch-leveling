import reflex as rx
from kinch_leveling_reflex.api.api import get_pbs, get_pr_kinch, get_wca_kinch
from kinch_leveling_reflex.serializers import Category, Record
from kinch_leveling_reflex.states.WCAState import WCAState
from kinch_leveling_reflex.states.AuthState import AuthState

class HeaderState(rx.State):
  pb_kinch: float
  pr_kinch: float
  nr_kinch: float
  wr_kinch: float
  xp_total: int
  wca_categories: list[Record]  
  wca_id: str
  
  @rx.event
  async def load_data(self):
    wca_state = await self.get_state(WCAState)
    self.wca_categories = wca_state.wca_categories
    auth_state = await self.get_state(AuthState)
    self.wca_id = auth_state.wca_id

    pbs, xp_scores = await get_pbs(self.wca_id)
    prs = await get_pr_kinch(self.wca_categories, self.wca_id)
    nr_records = wca_state.nr_records
    wr_records = wca_state.wr_records
    nrs = get_wca_kinch(nr_records, self.wca_id)
    wrs = get_wca_kinch(wr_records, self.wca_id)

    pb_sum = 0
    pr_sum = 0
    nr_sum = 0
    wr_sum = 0
    xp_sum = 0
    
    for pb in pbs.values():
      pb_sum += pb
      
    for pr in prs.values():
      pr_sum += pr
      
    for nr in nrs.values():
      nr_sum += nr
      
    for wr in wrs.values():
      wr_sum += wr
      
    for xp in xp_scores.values():
      xp_sum += xp
    
    if self.wca_id:
      self.pb_kinch = round(pb_sum / len(pbs), 2)
      self.pr_kinch = round(pr_sum / len(prs), 2)
      self.nr_kinch = round(nr_sum / len(nrs), 2)
      self.wr_kinch = round(wr_sum / len(wrs), 2)
      self.xp_total = xp_sum