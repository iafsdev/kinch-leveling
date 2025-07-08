import requests
from kinch_leveling_reflex.serializers import Category, Record

class WcaAPI():
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/"
        self.categories_map = {
            "222": "2x2",
            "333": "3x3",
            "444": "4x4",
            "555": "5x5",
            "666": "6x6",
            "777": "7x7",
            "333bf": "3BLD",
            "pyram": "Pyraminx",
            "skewb": "Skewb",
            "minx": "Megaminx",
            "clock": "Clock",
            "444bf": "4BLD",
            "555bf": "5BLD",
            "333oh": "OH",
            "333fm": "FMC",
            "sq1": "Square-1",
            "333mbf": "MBLD"
        }
        
    def get_events(self) -> list[Record]:
        response = requests.get(self.base_url + "events.json")
        categories = []
        
        for category in response.json()['items']:
            category_id = category['id']
            if category_id in self.categories_map:
                categories.append(Record(id=category_id, name=self.categories_map[category_id], type=""))
            
        return categories
    
    def get_nr_record(self, category_id: str, type: str) -> float:
        response = requests.get(self.base_url + f"rank/MX/{type}/{category_id}.json")
        result = response.json()['items'][0]['best']
        result = float(str(result)[:-2] + '.' + str(result)[-2:]) if result >= 100 else float('0.' + str(result))
        return result
    
    def get_wr_record(self, category_id: str, type: str) -> float:
        response = requests.get(self.base_url + f"rank/world/{type}/{category_id}.json")
        result = response.json()['items'][0]['best']
        result = float(str(result)[:-2] + '.' + str(result)[-2:]) if result >= 100 else float('0.' + str(result))
        return result
    
    def get_pr_records(self, wca_id:str='2023SEGO03'):
        response = requests.get(self.base_url + f"persons/{wca_id}.json")
        result = response.json()['rank']
        return result