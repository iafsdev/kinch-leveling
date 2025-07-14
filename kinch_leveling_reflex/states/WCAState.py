import reflex as rx
from kinch_leveling_reflex.api.api import get_wca_events, get_wr_records, get_nr_records, get_wca_kinch
from kinch_leveling_reflex.serializers import Record, WCARecord


class WCAState(rx.State):
  @rx.var(cache=True)
  def wca_categories(self) -> list[Record]:
    return get_wca_events()
  
  @rx.var(cache=True)
  def wr_records(self) -> list[WCARecord]:
    return get_wr_records(self.wca_categories)
  
  @rx.var(cache=True)
  def nr_records(self) -> list[WCARecord]:
    return get_nr_records(self.wca_categories)
  
  @rx.var(cache=True)
  def wr_kinch(self) -> dict[str, float]:
    return get_wca_kinch(self.wr_records)
  
  @rx.var(cache=True)
  def nr_kinch(self) -> dict[str, float]:
    return get_wca_kinch(self.nr_records)