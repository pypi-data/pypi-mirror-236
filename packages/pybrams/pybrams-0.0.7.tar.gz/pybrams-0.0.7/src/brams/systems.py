from typing import Dict, Any
import json_fix # type: ignore
from dataclasses import dataclass
from .locations import Location, get as get_location
from .api import base_url

import requests
import json
import datetime
from .cache import Cache

endpoint = f"{base_url}/system.php"

@dataclass
class System:

    system_code: str
    name: str
    start: str
    end: str
    antenna: int
    location_url: str
    location_code: str

    def __json__(self) -> Dict[str, Any]:

        return {
            "system_code": self.system_code,
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "antenna": self.antenna,
            "location_url": self.location_url,
            "location_code": self.location_code
        }

    def location(self) -> Location | None:

        from .locations import get as get_location
        return get_location(self.location_code) 
        

def get(location: Location | None = None, system_code: str | None = None) -> System | Dict[str, System] | None:

    if location:

        cached_systems = Cache.get("systems")

        if cached_systems:

            json_systems = [system for system in json.loads(cached_systems).get("data").values() if system["location_code"] == location.location_code]

        else:

            payload = {
                "location_code": location.location_code
            }

            response = requests.post(endpoint, data=payload)
            json_systems =  response.json()

        if isinstance(json_systems, list):

            systems: dict[str, System] = {}
            json_systems = { system["system_code"] : system for system in json_systems }

            for code, json_system in json_systems.items():

                systems[code] = System(*json_system.values())

            return systems

        else:

            return System(*json_systems.values())

    elif system_code:

        system = None

        for key in [system_code, "systems"]:

            json_system = Cache.get(key)

            if json_system:

                system = json.loads(json_system).get("data").get(system_code)

                if system:

                    break
                
        if not system:

            payload = {
                "system_code": system_code
            }

            response = requests.post(endpoint, data=payload)
            json_system =  response.json()

            json_content = {
                "date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                "data": {
                    system_code: json_system
                }
            }
            
            Cache.cache(system_code, json.dumps(json_content, indent=4))
            system = json_system

        return System(*system.values()) if system else None
    
    else: 

        return None


def all() -> Dict[str, System]:

    json_systems = Cache.get("systems")

    if not json_systems:

        response = requests.get(endpoint)
        json_systems =  response.json()
        json_systems = { system["system_code"] : system for system in json_systems }
    
        json_content = {
            "date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "data": json_systems
        }

        Cache.cache("systems", json.dumps(json_content, indent=4))

    else:

        json_systems = json.loads(json_systems).get("data")

    systems: dict[str, System] = {}

    for code, json_system in json_systems.items():

        systems[code] = System(*json_system.values())

    return systems
