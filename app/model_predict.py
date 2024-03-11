"""Model predictions."""
import requests


def tree_count(place, year):
    """Parser for OSM."""
    town = place.split(", ")[0]
    url = r"http://overpass-api.de/api/interpreter"
    query = f"""[out:json][date:'{year}-01-01T00:00:00Z'][maxsize:2000000000];
    area["name:en"="{town}"]->.searchArea;
    (node["natural"="tree"](area.searchArea);); out count;"""
    result = requests.post(url, data=query, timeout=60)
    t = result.text
    cap = "total"
    for i in range(len(t)):
        if t[i : i + len(cap)] == cap:
            t = t[i + len(cap) + 4 :]
            for j in range(len(t)):  # pylint: disable=C0200
                if not t[j].isdigit():
                    return int(t[:j])
    return 0
