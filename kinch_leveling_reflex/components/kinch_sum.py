import reflex as rx
from kinch_leveling_reflex.states.HeaderState import HeaderState

def kinch_sum() -> rx.Component:
  return rx.flex(
    rx.text(f'PB Kinch: {HeaderState.pb_kinch}'),
    rx.text(f'PR Kinch: {HeaderState.pr_kinch}'),
    rx.text(f'NR Kinch: {HeaderState.nr_kinch}'),
    rx.text(f'WR Kinch: {HeaderState.wr_kinch}'),
    rx.text(f'XP: {HeaderState.xp_total}'),
    justify='center',
    spacing='9',
  ),