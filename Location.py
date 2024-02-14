import streamlit as st
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.distance import geodesic

def get_user_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        return data['loc'].split(',')
    except:
        st.error("Error: Unable to detect your location.")
        return None, None
    
def find_nearby_places(lat, lon, place_type, radius):
    geolocator = Nominatim(user_agent="nearby_search")
    
    for _ in range(3):
        try:
            location = geolocator.reverse((lat, lon))
            st.write(f"\nYour current location: {location}\n")
            break
        except GeocoderTimedOut:
            st.warning("Timeout error. Retrying...")
            continue
        except GeocoderUnavailable as e:
            st.error(f"Geocoding service unavailable. {e}")
            return
    
    query = f"{place_type} near {lat}, {lon}"
    
    try:
        places = geolocator.geocode(query, exactly_one=False, limit=None)
        if places:
            for place in places:
                place_coords = (place.latitude, place.longitude)
                place_distance = geodesic((lat, lon), place_coords).kilometers
                if place_distance <= radius:
                    st.write(f"{place.address} ({place_distance:.2f} km)")
        else:
            st.warning("No nearby places found for the given type.")
    except Exception as e:
        st.error(f"Error: Unable to fetch nearby places. {e}")

def main():
    st.title("Find Nearby Places")
    
    user_lat, user_lon = get_user_location()
    
    if user_lat is not None and user_lon is not None:
        place_type = st.text_input("What type of place are you looking for? (e.g., park, mall, ATM, hotel): ")
        search_radius = st.slider("Select the search radius (in kilometers):", 1, 50, 10, 1)
        
        if st.button("Find Nearby Places"):
            find_nearby_places(float(user_lat), float(user_lon), place_type, search_radius)

if __name__ == "__main__":
    main()
