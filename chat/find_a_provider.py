# chat/provider_search.py
"""
Healthcare Provider Search using real APIs
"""

import requests
from geopy.geocoders import Nominatim
from typing import List, Dict, Optional
import time

class ProviderSearcher:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="womens_health_app")
        
    def get_coordinates_from_zipcode(self, zipcode: str) -> Optional[tuple]:
        # zip -> coordinates (lat lon)
        try:
            location = self.geolocator.geocode(f"{zipcode}, USA")
            if location:
                return (location.latitude, location.longitude)
        except Exception as e:
            print(f"Error geocoding {zipcode}: {e}")
        return None
    
    def search_providers_overpass(self, lat: float, lon: float, radius_km: float = 25) -> List[Dict]:
        # use openstreetmap overpass api to find health providers in area

        providers = []
        
        # API query for healthcare 
        overpass_url = "http://overpass-api.de/api/interpreter"
        
        # search for healthcare facilities
        queries = [
            f'node["amenity"="hospital"](around:{radius_km*1000},{lat},{lon});',
            f'node["amenity"="clinic"](around:{radius_km*1000},{lat},{lon});',
            f'node["amenity"="doctors"](around:{radius_km*1000},{lat},{lon});',
            f'node["healthcare"="doctor"](around:{radius_km*1000},{lat},{lon});',
            f'node["healthcare"="clinic"](around:{radius_km*1000},{lat},{lon});',
            f'way["amenity"="hospital"](around:{radius_km*1000},{lat},{lon});',
            f'way["amenity"="clinic"](around:{radius_km*1000},{lat},{lon});',
        ]
        
        overpass_query = f"""
        [out:json][timeout:25];
        (
          {' '.join(queries)}
        );
        out body;
        >;
        out skel qt;
        """
        
        try:
            response = requests.post(overpass_url, data={'data': overpass_query}, timeout=30)
            data = response.json()
            
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                if 'name' in tags:
                    provider = {
                        'name': tags.get('name', 'Unknown'),
                        'type': self._categorize_provider(tags),
                        'address': self._format_address(tags),
                        'phone': tags.get('phone', 'N/A'),
                        'lat': element.get('lat', 0),
                        'lon': element.get('lon', 0),
                        'distance': self._calculate_distance(lat, lon, 
                                                            element.get('lat', 0), 
                                                            element.get('lon', 0))
                    }
                    providers.append(provider)
            
            # sort by distance
            providers.sort(key=lambda x: x['distance'])
            
        except Exception as e:
            print(f"Error searching providers: {e}")
        
        return providers
    
    def _categorize_provider(self, tags: dict) -> str:
        # type of provider
        if tags.get('amenity') == 'hospital':
            return 'Hospital'
        elif tags.get('healthcare') == 'clinic' or tags.get('amenity') == 'clinic':
            specialty = tags.get('healthcare:speciality', '')
            if 'gynecology' in specialty.lower() or 'obstetrics' in specialty.lower():
                return 'OB/GYN Clinic'
            elif 'mental' in specialty.lower() or 'psychology' in specialty.lower():
                return 'Mental Health Clinic'
            return 'Medical Clinic'
        elif tags.get('healthcare') == 'doctor':
            return 'Medical Practice'
        return 'Healthcare Facility'
    
    def _format_address(self, tags: dict) -> str:
        """Format address from OSM tags"""
        parts = []
        if 'addr:housenumber' in tags and 'addr:street' in tags:
            parts.append(f"{tags['addr:housenumber']} {tags['addr:street']}")
        elif 'addr:street' in tags:
            parts.append(tags['addr:street'])
        
        if 'addr:city' in tags:
            parts.append(tags['addr:city'])
        if 'addr:state' in tags:
            parts.append(tags['addr:state'])
        if 'addr:postcode' in tags:
            parts.append(tags['addr:postcode'])
        
        return ', '.join(parts) if parts else 'Address not available'
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # find the number of miles between two points 
        from math import radians, sin, cos, sqrt, atan2
        
        # radius of the earth (miles)
        R = 3959  
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return round(R * c, 1)
    
    def add_planned_parenthood_locations(self, providers: List[Dict], state: str = None) -> List[Dict]:
        # include plannedparenthood locations (??)
        # idk if pp has an api for locations 
        pp_locations = [
            {
                'name': 'Planned Parenthood',
                'type': "Women's Health Clinic",
                'address': 'Check plannedparenthood.org for nearest location',
                'phone': '1-800-230-7526',
                'website': 'https://www.plannedparenthood.org/health-center',
                'distance': 'N/A'
            }
        ]
        return providers + pp_locations
    
    def get_mental_health_resources(self) -> List[Dict]:
        # keep the resources that pommie redirects to from before 
        return [
            {
                'name': 'National Alliance on Mental Illness (NAMI)',
                'type': 'Mental Health Support',
                'phone': '1-800-950-NAMI (6264)',
                'website': 'https://www.nami.org',
                'description': 'Free mental health support and resources'
            },
            {
                'name': 'SAMHSA National Helpline',
                'type': 'Mental Health & Substance Abuse',
                'phone': '1-800-662-4357',
                'website': 'https://www.samhsa.gov/find-help/national-helpline',
                'description': '24/7 free and confidential treatment referral'
            },
            {
                'name': '988 Suicide & Crisis Lifeline',
                'type': 'Crisis Support',
                'phone': '988',
                'website': 'https://988lifeline.org',
                'description': '24/7 crisis support for mental health emergencies'
            },
            {
                'name': 'Postpartum Support International',
                'type': 'Maternal Mental Health',
                'phone': '1-800-944-4773',
                'website': 'https://www.postpartum.net',
                'description': 'Support for pregnancy and postpartum mental health'
            }
        ]