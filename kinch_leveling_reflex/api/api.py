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
    