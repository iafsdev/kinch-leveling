import reflex as rx
from kinch_leveling_reflex.api.SupabaseAPI import SupabaseAPI
from kinch_leveling_reflex.api.WcaAPI import WcaAPI
from kinch_leveling_reflex.api.TnoodleAPI import TnoodleAPI
from fastapi import FastAPI
from kinch_leveling_reflex.serializers import Category, Time, Record, WCARecord
from kinch_leveling_reflex.utils import format_time

fastapi_app = FastAPI()
supabase = SupabaseAPI()
wca = WcaAPI()
tnoodle = TnoodleAPI()

@fastapi_app.get("/get_categories")
async def get_categories() -> list[Category]:
    return supabase.get_categories()

@fastapi_app.get("/get_kaizen")
async def get_kaizen(wca_id: str) -> dict[str, str]:
    data = supabase.get_times(wca_id)
    kaizen = {}
    
    for time in data:
        if time.proportion == 0:
            kaizen[time.category] = "00.000"
        else:
            kaizen_calculation = round(time.actual_time / time.proportion, 3)
            kaizen[time.category] = format_time(kaizen_calculation)
    
    return kaizen

@fastapi_app.get("/get_times")
async def get_times(wca_id: str) -> list[Time]:
    return supabase.get_times(wca_id)

@fastapi_app.patch("/update_time")
async def update_time(category: str, actual_time: float, goal_time: float, proportion: float, xp: int, wca_id: str) -> bool:
    categories = supabase.get_categories()
    category_id = 0
    for item in categories:
        if item.name == category:
            category_id = item.id
            break

    return supabase.update_time(category_id, actual_time, goal_time, proportion, xp, wca_id)

@fastapi_app.get("/get_pbs")
async def get_pbs(wca_id: str) -> dict[str, float]:
    data = supabase.get_times(wca_id)
    pbs = {}
    xp = {}
    
    for time in data:
        if time.actual_time == 0:
            pbs[time.category] = 0
        else:
            pbs[time.category] = round((time.goal_time * 100) / time.actual_time, 2)
            
        xp[time.category] = time.xp
    
    return pbs, xp

@fastapi_app.get("/get_wca_events")
def get_wca_events() -> list[Record]:
    wca_categories = wca.get_events()
    supabase_categories = supabase.get_categories()
    
    for wca_category in wca_categories:
        for supabase_category in supabase_categories:
            if wca_category.name == supabase_category.name:
                wca_category.type = supabase_category.type
                break

    return wca_categories

def get_nr_records(wca_categories: list[Category]) -> list[WCARecord]:
    nr_records = []
    
    for wca_category in wca_categories:
        average = wca.get_nr_record(wca_category.id, "average") if wca_category.name != "MBLD" else 0
        single = wca.get_nr_record(wca_category.id, "single")
        
        nr_records.append(
            WCARecord(
                category=wca_category.name,
                average=average,
                single=single,
                type=wca_category.type
            )
        )
    return nr_records

def get_wr_records(wca_categories: list[Category]) -> list[WCARecord]:
    wr_records = []
    
    for wca_category in wca_categories:
        average = wca.get_wr_record(wca_category.id, "average") if wca_category.name != "MBLD" else 0
        single = wca.get_wr_record(wca_category.id, "single")
        
        wr_records.append(
            WCARecord(
                category=wca_category.name,
                average=average,
                single=single,
                type=wca_category.type
            )
        )
    return wr_records
            
@fastapi_app.get("/get_wca_kinch")
def get_wca_kinch(records: list[WCARecord], wca_id: str) -> dict[str, float]:
    data = supabase.get_times(wca_id)
    kinch = {}
    
    for time in data:
        if time.actual_time == 0:
            kinch[time.category] = 0
        else:
            for record in records:
                if time.category == record.category:
                    if record.type == "Average/Single":
                        average = record.average
                        single = record.single
                        kinch_average = round((average * 100) / time.actual_time, 2)
                        kinch_single = round((single * 100) / time.actual_time, 2)
                        kinch[time.category] = kinch_average if kinch_average < kinch_single else kinch_single
                    else:
                        if record.type == "Average":
                            average = record.average
                            kinch[time.category] = round((average * 100) / time.actual_time, 2)
                        elif record.type == "Single":
                            single = record.single
                            kinch[time.category] = round((single * 100) / time.actual_time, 2)
                    break
                
    return kinch

async def get_pr_kinch(wca_categories: list[Category], wca_id: str) -> dict[str, float]:
    data = supabase.get_times(wca_id)
    pr_kinch = {}
    prs = wca.get_pr_records()
    
    for time in data:
        if time.actual_time == 0:
            pr_kinch[time.category] = 0
        else:
            for wca_category in wca_categories:
                if time.category == wca_category.name:
                    pr_record = 0
                    if wca_category.type == "Average/Single":
                        average = next((s['best'] for s in prs['averages'] if s['eventId'] == wca_category.id), 0)
                        average = float(str(average)[:-2] + '.' + str(average)[-2:]) if average >= 100 else float('0.' + str(average))
                        single = next((s['best'] for s in prs['singles'] if s['eventId'] == wca_category.id), 0)
                        single = float(str(single)[:-2] + '.' + str(single)[-2:]) if single >= 100 else float('0.' + str(single))
                        kinch_average = round((average * 100) / time.actual_time, 2) if average != 0 else 0
                        kinch_single = round((single * 100) / time.actual_time, 2) if single != 0 else 0
                        pr_kinch[time.category] = kinch_average if kinch_average < kinch_single and kinch_average != 0 else kinch_single
                    else:
                        record = next((s['best'] for s in prs[wca_category.type.lower()+'s'] if s['eventId'] == wca_category.id), 0)
                        record = float(str(record)[:-2] + '.' + str(record)[-2:]) if record >= 100 else float('0.' + str(record))
                        pr_kinch[time.category] = round((record * 100) / time.actual_time, 2) if record != 0 else 0
                    break
                
    return pr_kinch
            
def create_new_profile(wca_id: str) -> bool:
    insertions = []
    
    for i in range(1,18):
        insertions.append({
            "user_id": wca_id,
            'actual_time': 0,
            'goal_time': 0,
            'kaizen_proportion': 0,
            'category_id': i,
            'xp': 0
        })

    return supabase.new_profile(insertions)

def check_profile(wca_id: str) -> bool:
    return supabase.check_profile(wca_id)

def get_scramble(category:str) -> tuple[str, str]:
    return tnoodle.get_scramble(category)