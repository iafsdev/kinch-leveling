import reflex as rx
from kinch_leveling_reflex.api.api import get_pbs, get_nr_kinch, get_wr_kinch

class HeaderState(rx.State):
  pb_kinch: float
  pr_kinch: float = 0.0
  nr_kinch: float
  wr_kinch: float
  
  @rx.event
  async def load_data(self):
    pbs = await get_pbs()
    nrs = await get_nr_kinch()
    wrs = await get_wr_kinch()
    
    pb_sum = 0
    nr_sum = 0
    wr_sum = 0
    
    for pb in pbs.values():
      pb_sum += pb
      
    for nr in nrs.values():
      nr_sum += nr
      
    for wr in wrs.values():
      wr_sum += wr
    
    self.pb_kinch = round(pb_sum / len(pbs), 2)
    self.nr_kinch = round(nr_sum / len(nrs), 2)
    self.wr_kinch = round(wr_sum / len(wrs), 2)