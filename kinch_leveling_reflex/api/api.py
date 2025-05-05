import reflex as rx
from kinch_leveling_reflex.api.SupabaseAPI import SupabaseAPI
from fastapi import FastAPI
from kinch_leveling_reflex.serializers import Category, Time
from kinch_leveling_reflex.utils import format_time

fastapi_app = FastAPI()
supabase = SupabaseAPI()

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

    