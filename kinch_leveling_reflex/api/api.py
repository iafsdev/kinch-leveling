import reflex as rx
from kinch_leveling_reflex.api.SupabaseAPI import SupabaseAPI
from kinch_leveling_reflex.api.WcaAPI import WcaAPI
from fastapi import FastAPI
from kinch_leveling_reflex.serializers import Category, Time, Record
from kinch_leveling_reflex.utils import format_time

fastapi_app = FastAPI()
supabase = SupabaseAPI()
wca = WcaAPI()

@fastapi_app.get("/get_categories")
async def get_categories() -> list[Category]:
    return supabase.get_categories()

@fastapi_app.get("/get_kaizen")
async def get_kaizen() -> dict[str, str]:
    data = supabase.get_times()
    kaizen = {}
    
    for time in data:
        if time.proportion == 0:
            kaizen[time.category] = "00.000"
        else:
            kaizen_calculation = round(time.actual_time / time.proportion, 3)
            kaizen[time.category] = format_time(kaizen_calculation)
    
    return kaizen

@fastapi_app.get("/get_times")
async def get_times() -> list[Time]:
    return supabase.get_times()

@fastapi_app.patch("/update_time")
async def update_time(category: str, actual_time: float, goal_time: float, proportion: float) -> bool:
    categories = supabase.get_categories()
    category_id = 0
    for item in categories:
        if item.name == category:
            category_id = item.id
            break
    
    return supabase.update_time(category_id, actual_time, goal_time, proportion)

@fastapi_app.get("/get_pbs")
async def get_pbs() -> dict[str, float]:
    data = supabase.get_times()
    pbs = {}
    
    for time in data:
        if time.actual_time == 0:
            pbs[time.category] = 0
        else:
            pbs[time.category] = round((time.goal_time * 100) / time.actual_time, 2)
    
    return pbs

@fastapi_app.get("/get_wca_events")
async def get_wca_events() -> list[Category]:
    wca_categories = wca.get_events()
    supabase_categories = supabase.get_categories()
    
    for wca_category in wca_categories:
        for supabase_category in supabase_categories:
            if wca_category.name == supabase_category.name:
                wca_category.type = supabase_category.type
                break

    return wca_categories

@fastapi_app.get("/get_nr_kinch")
async def get_nr_kinch() -> dict[str, float]:
    wca_categories = await get_wca_events()
    data = supabase.get_times()
    nr_kinch = {}
    
    for time in data:
        if time.actual_time == 0:
            nr_kinch[time.category] = 0
        else:
            for wca_category in wca_categories:
                if time.category == wca_category.name:
                    nr_record = 0
                    if wca_category.type == "Average/Single":
                        average = wca.get_nr_record(wca_category.id, "average")
                        single = wca.get_nr_record(wca_category.id, "single")
                        kinch_average = round((average * 100) / time.actual_time, 2)
                        kinch_single = round((single * 100) / time.actual_time, 2)
                        nr_kinch[time.category] = kinch_average if kinch_average < kinch_single else kinch_single
                    else:
                        record = wca.get_nr_record(wca_category.id, wca_category.type.lower())
                        nr_kinch[time.category] = round((record * 100) / time.actual_time, 2)
                    break
                
    return nr_kinch
            
@fastapi_app.get("/get_wr_kinch")
async def get_wr_kinch() -> dict[str, float]:
    wca_categories = await get_wca_events()
    data = supabase.get_times()
    wr_kinch = {}
    
    for time in data:
        if time.actual_time == 0:
            wr_kinch[time.category] = 0
        else:
            for wca_category in wca_categories:
                if time.category == wca_category.name:
                    wr_record = 0
                    if wca_category.type == "Average/Single":
                        average = wca.get_wr_record(wca_category.id, "average")
                        single = wca.get_wr_record(wca_category.id, "single")
                        kinch_average = round((average * 100) / time.actual_time, 2)
                        kinch_single = round((single * 100) / time.actual_time, 2)
                        wr_kinch[time.category] = kinch_average if kinch_average < kinch_single else kinch_single
                    else:
                        record = wca.get_wr_record(wca_category.id, wca_category.type.lower())
                        wr_kinch[time.category] = round((record * 100) / time.actual_time, 2)
                    break
                
    return wr_kinch

async def get_pr_kinch() -> dict[str, float]:
    wca_categories = await get_wca_events()
    data = supabase.get_times()
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
            
        