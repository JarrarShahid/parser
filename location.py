# location_extractor.py
# Extract cities, countries, continents from free text.
# Uses pycountry, geonamescache and spaCy when available; falls back to a small built-in set otherwise.

import re
import unicodedata
from collections import defaultdict

# Optional libs (not required; function will fall back if missing)
try:
    import pycountry
except Exception:
    pycountry = None

try:
    import geonamescache as gc
except Exception:
    gc = None

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])
    except Exception:
        nlp = None
except Exception:
    nlp = None


# ---------- Small stable list of continents ----------
CONTINENTS = {
    "africa": "Africa",
    "antarctica": "Antarctica",
    "asia": "Asia",
    "europe": "Europe",
    "north america": "North America",
    "south america": "South America",
    "oceania": "Oceania",
    "australia": "Oceania",  # accept either
}

# manual country alias mapping (common short forms)
_MANUAL_COUNTRY_ALIASES = {
    "usa": "United States",
    "us": "United States",
    "u.s.": "United States",
    "u.s.a.": "United States",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "uae": "United Arab Emirates",
    "south korea": "Korea, Republic of",
    "north korea": "Korea, Democratic People's Republic of",
    "ivory coast": "Côte d'Ivoire",
    "czech republic": "Czechia",
    "russia": "Russian Federation",
    "vietnam": "Viet Nam",
}

# ---------- Helper normalizers ----------
def _strip_accents(txt: str) -> str:
    if not txt:
        return txt
    nfkd = unicodedata.normalize("NFKD", txt)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def _safe_lower(s: str) -> str:
    return _strip_accents(s).lower().strip()

_word_regex = re.compile(r"[A-Za-z0-9\u00C0-\u017F']+")


def _tokenize(text: str):
    # produce tokens (keep hyphen/apostrophe inside words)
    t = _strip_accents(text)
    t = re.sub(r"[^\w\s'\-]", " ", t)
    return [tok for tok in re.findall(_word_regex, t)]


# ---------- Build country and city maps (normalized keys) ----------
country_map = {}
if pycountry:
    for c in pycountry.countries:
        names = {c.name}
        if getattr(c, "official_name", None):
            names.add(c.official_name)
        if getattr(c, "common_name", None):
            names.add(c.common_name)
        for n in names:
            if not n:
                continue
            country_map[_safe_lower(n)] = {"name": c.name, "alpha2": getattr(c, "alpha_2", None), "alpha3": getattr(c, "alpha_3", None)}
    for k, v in _MANUAL_COUNTRY_ALIASES.items():
        country_map.setdefault(_safe_lower(k), {"name": v, "alpha2": None, "alpha3": None})
elif gc:
    gcobj = gc.GeonamesCache()
    for code, info in gcobj.get_countries().items():
        country_map[_safe_lower(info["name"])] = {"name": info["name"], "alpha2": code, "alpha3": None}
    for k, v in _MANUAL_COUNTRY_ALIASES.items():
        country_map.setdefault(_safe_lower(k), {"name": v, "alpha2": None, "alpha3": None})
else:
    # Minimal fallback (install pycountry for full coverage)
    fallback = [
        ("Pakistan", "PK"), ("United States", "US"), ("United Kingdom", "GB"),
        ("India", "IN"), ("Brazil", "BR"), ("Canada", "CA"), ("Australia", "AU"),
        ("Germany", "DE"), ("France", "FR"), ("China", "CN"),
    ]
    for name, code in fallback:
        country_map[_safe_lower(name)] = {"name": name, "alpha2": code, "alpha3": None}
    for k, v in _MANUAL_COUNTRY_ALIASES.items():
        country_map.setdefault(_safe_lower(k), {"name": v, "alpha2": None, "alpha3": None})

cities_map = defaultdict(list)
max_city_token_len = 1
if gc:
    gcobj = gc.GeonamesCache()
    try:
        cities = gcobj.get_cities()
    except Exception:
        cities = {}
    for gid, info in cities.items():
        name = info.get("name")
        if not name:
            continue
        key = _safe_lower(name)
        cities_map[key].append({
            "name": name,
            "countrycode": info.get("countrycode"),
            "geonameid": gid,
            "admin1": info.get("admin1code"),
        })
    if cities_map:
        max_city_token_len = max(len(k.split()) for k in cities_map.keys())
else:
    # small fallback list of common cities
    fallback_cities = [
        ("New York", "US"), ("Los Angeles", "US"), ("Karachi", "PK"),
        ("Lahore", "PK"), ("London", "GB"), ("Paris", "FR"), ("Berlin", "DE"),
        ("Tokyo", "JP"), ("São Paulo", "BR"), ("Sydney", "AU"), ("Toronto", "CA"),
    ]
    for name, cc in fallback_cities:
        cities_map[_safe_lower(name)].append({"name": name, "countrycode": cc, "geonameid": None, "admin1": None})
    max_city_token_len = max(len(k.split()) for k in cities_map.keys())

MAX_NGRAM = min(max(5, max_city_token_len), 6)


# ---------- Core function ----------
def extract_locations(text: str, prefer_ner: bool = True):
    """
    Extract cities, countries and continents from `text`.
    Returns: { "countries": [...], "cities": [...], "continents": [...], "ambiguous": [...] }
    """
    results = {"countries": [], "cities": [], "continents": [], "ambiguous": []}
    if not text or not text.strip():
        return results

    # 1) Use spaCy NER to get candidates (if available and preferred)
    candidates = []
    if prefer_ner and nlp:
        try:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ("GPE", "LOC"):
                    candidates.append((ent.text, ent.start_char, ent.end_char))
        except Exception:
            candidates = []

    # Prepare tokens (accent-stripped)
    normalized_for_scan = _strip_accents(text)
    scan_tokens = _tokenize(normalized_for_scan)
    joined_lower = " ".join(scan_tokens).lower()

    if not candidates:
        # n-gram scanning for country/city/continent names
        n_tokens = len(scan_tokens)
        for n in range(min(MAX_NGRAM, n_tokens), 0, -1):
            for i in range(0, n_tokens - n + 1):
                phrase = " ".join(scan_tokens[i: i + n]).strip()
                key = _safe_lower(phrase)
                if key.isdigit():
                    continue
                # continents (small set)
                if key in CONTINENTS and key not in [c["canonical"].lower() for c in results["continents"]]:
                    results["continents"].append({"text": phrase, "canonical": CONTINENTS[key]})
                    continue
                # countries
                if key in country_map:
                    meta = country_map[key]
                    results["countries"].append({"text": phrase, "canonical": meta.get("name"), "alpha2": meta.get("alpha2"), "alpha3": meta.get("alpha3")})
                    continue
                # cities
                if key in cities_map:
                    for crecord in cities_map[key]:
                        results["cities"].append({
                            "text": phrase,
                            "name": crecord.get("name"),
                            "countrycode": crecord.get("countrycode"),
                            "geonameid": crecord.get("geonameid"),
                            "admin1": crecord.get("admin1")
                        })
                    continue
        # continent substring detection
        for cont_key, cont_name in CONTINENTS.items():
            if re.search(r"\b" + re.escape(cont_key) + r"\b", joined_lower):
                if cont_name not in [c["canonical"] for c in results["continents"]]:
                    results["continents"].append({"text": cont_key, "canonical": cont_name})
    else:
        # Map spaCy candidates to maps
        for ctext, s, e in candidates:
            key = _safe_lower(ctext)
            if key in CONTINENTS:
                results["continents"].append({"text": ctext, "canonical": CONTINENTS[key]})
                continue
            if key in country_map:
                meta = country_map[key]
                results["countries"].append({"text": ctext, "canonical": meta.get("name"), "alpha2": meta.get("alpha2"), "alpha3": meta.get("alpha3"), "start": s, "end": e})
                continue
            if key in cities_map:
                for crecord in cities_map[key]:
                    results["cities"].append({"text": ctext, "name": crecord.get("name"), "countrycode": crecord.get("countrycode"), "geonameid": crecord.get("geonameid"), "start": s, "end": e})
                continue
            # try fuzzy substring country match
            for cname, meta in country_map.items():
                if key in cname:
                    results["countries"].append({"text": ctext, "canonical": meta.get("name"), "alpha2": meta.get("alpha2"), "alpha3": meta.get("alpha3"), "start": s, "end": e})
                    break
            # try fuzzy city match (limited)
            for cityname in list(cities_map.keys())[:10000]:
                if key in cityname:
                    for crecord in cities_map[cityname]:
                        results["cities"].append({"text": ctext, "name": crecord.get("name"), "countrycode": crecord.get("countrycode"), "geonameid": crecord.get("geonameid"), "start": s, "end": e})
                    break

    # dedupe results
    def _dedupe(list_of_dicts, keys):
        seen = set()
        out = []
        for d in list_of_dicts:
            k = tuple((d.get(k) or "") for k in keys)
            if k not in seen:
                out.append(d)
                seen.add(k)
        return out

    results["countries"] = _dedupe(results["countries"], ["canonical", "alpha2", "alpha3", "text"])
    results["cities"] = _dedupe(results["cities"], ["name", "countrycode", "geonameid", "text"])
    results["continents"] = _dedupe(results["continents"], ["canonical", "text"])

    # mark ambiguous names matched as both city and country
    country_names_lower = {_safe_lower(c.get("canonical") or c.get("text")) for c in results["countries"]}
    city_names_lower = {_safe_lower(c.get("name") or c.get("text")) for c in results["cities"]}
    for name in country_names_lower & city_names_lower:
        results["ambiguous"].append({"text": name, "reason": "Matched as both country and city/region"})

    return results


# Simple demo when run directly:
if __name__ == "__main__":
    examples = [
        "I traveled from New York to Paris last summer.",
        "She lives in Karachi, Pakistan.",
        "Our office is in São Paulo, Brazil.",
        "He mentioned Europe and Asia during the talk.",
        "I will be in the U.S. next month.",
        "Visited the state of Georgia and the country Georgia as well.",
        "Let's meet in the UK or in London.",
    ]
    for e in examples:
        print("-" * 60)
        print("Input:", e)
        r = extract_locations(e)
        print("Countries:", r["countries"])
        print("Cities   :", r["cities"])
        print("Continents:", r["continents"])
        if r["ambiguous"]:
            print("Ambiguous:", r["ambiguous"])
        print()
