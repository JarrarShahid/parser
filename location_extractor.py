# location_extractor.py
# Class-based location extractor: returns simple list of names (city, country, continent)

import re
import unicodedata
from collections import defaultdict

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


class LocationExtractor:
    CONTINENTS = {
        "africa": "Africa",
        "antarctica": "Antarctica",
        "asia": "Asia",
        "europe": "Europe",
        "north america": "North America",
        "south america": "South America",
        "oceania": "Oceania",
        "australia": "Oceania",
    }

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

    def __init__(self, prefer_ner: bool = True):
        self.prefer_ner = prefer_ner
        self.country_map = self._build_country_map()
        self.cities_map, self.max_city_token_len = self._build_city_map()
        self.MAX_NGRAM = min(max(5, self.max_city_token_len), 6)

    # ---------------- helpers ----------------
    def _strip_accents(self, txt: str) -> str:
        nfkd = unicodedata.normalize("NFKD", txt)
        return "".join([c for c in nfkd if not unicodedata.combining(c)])

    def _safe_lower(self, s: str) -> str:
        return self._strip_accents(s).lower().strip()

    def _tokenize(self, text: str):
        t = self._strip_accents(text)
        t = re.sub(r"[^\w\s'\-]", " ", t)
        return re.findall(r"[A-Za-z0-9\u00C0-\u017F']+", t)

    # ---------------- build maps ----------------
    def _build_country_map(self):
        country_map = {}
        if pycountry:
            for c in pycountry.countries:
                names = {c.name}
                if getattr(c, "official_name", None):
                    names.add(c.official_name)
                if getattr(c, "common_name", None):
                    names.add(c.common_name)
                for n in names:
                    if n:
                        country_map[self._safe_lower(n)] = c.name
            for k, v in self._MANUAL_COUNTRY_ALIASES.items():
                country_map[self._safe_lower(k)] = v
        elif gc:
            gcobj = gc.GeonamesCache()
            for _, info in gcobj.get_countries().items():
                country_map[self._safe_lower(info["name"])] = info["name"]
            for k, v in self._MANUAL_COUNTRY_ALIASES.items():
                country_map[self._safe_lower(k)] = v
        else:
            fallback = ["Pakistan", "United States", "United Kingdom", "India",
                        "Brazil", "Canada", "Australia", "Germany", "France", "China"]
            for name in fallback:
                country_map[self._safe_lower(name)] = name
            for k, v in self._MANUAL_COUNTRY_ALIASES.items():
                country_map[self._safe_lower(k)] = v
        return country_map

    def _build_city_map(self):
        cities_map = defaultdict(list)
        max_city_token_len = 1
        if gc:
            gcobj = gc.GeonamesCache()
            try:
                cities = gcobj.get_cities()
            except Exception:
                cities = {}
            for _, info in cities.items():
                name = info.get("name")
                if name:
                    cities_map[self._safe_lower(name)].append(name)
            if cities_map:
                max_city_token_len = max(len(k.split()) for k in cities_map.keys())
        else:
            fallback_cities = ["New York", "Los Angeles", "Karachi", "Lahore", "London",
                               "Paris", "Berlin", "Tokyo", "São Paulo", "Sydney", "Toronto"]
            for name in fallback_cities:
                cities_map[self._safe_lower(name)].append(name)
            max_city_token_len = max(len(k.split()) for k in cities_map.keys())
        return cities_map, max_city_token_len

    # ---------------- main extractor ----------------
    def extract(self, text: str):
        results = []

        if not text or not text.strip():
            return results

        candidates = []
        if self.prefer_ner and nlp:
            try:
                doc = nlp(text)
                for ent in doc.ents:
                    if ent.label_ in ("GPE", "LOC"):
                        candidates.append(ent.text)
            except Exception:
                pass

        tokens = self._tokenize(text)
        joined_lower = " ".join(tokens).lower()

        if not candidates:
            n_tokens = len(tokens)
            for n in range(min(self.MAX_NGRAM, n_tokens), 0, -1):
                for i in range(0, n_tokens - n + 1):
                    phrase = " ".join(tokens[i:i + n])
                    key = self._safe_lower(phrase)
                    if key in self.CONTINENTS:
                        results.append(self.CONTINENTS[key])
                    elif key in self.country_map:
                        results.append(self.country_map[key])
                    elif key in self.cities_map:
                        results.extend(self.cities_map[key])
            for cont_key, cont_name in self.CONTINENTS.items():
                if re.search(r"\b" + re.escape(cont_key) + r"\b", joined_lower):
                    if cont_name not in results:
                        results.append(cont_name)
        else:
            for ctext in candidates:
                key = self._safe_lower(ctext)
                if key in self.CONTINENTS:
                    results.append(self.CONTINENTS[key])
                elif key in self.country_map:
                    results.append(self.country_map[key])
                elif key in self.cities_map:
                    results.extend(self.cities_map[key])

        # Deduplicate while keeping order
        seen = set()
        final = []
        for r in results:
            if r not in seen:
                final.append(r)
                seen.add(r)
        return final


# extractor = LocationExtractor()
# locations = extractor.extract("She lives in Karachi, Pakistan.")
# print(locations)  # ['Karachi', 'Pakistan']
