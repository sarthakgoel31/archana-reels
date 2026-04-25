"""
Content engine — picks today's spiritual content based on date and type.
Uses date-based rotation to cycle through temples, poojas, rashis, etc.
"""

import random
from datetime import date, datetime
from dataclasses import dataclass, field
from typing import Optional

from .data import (
    DAY_DEITY_MAP, TEMPLES, POOJAS, RASHIS, NAVGRAH,
    HOOKS, CTAS, SOFT_CTAS, TITHIS, NAKSHATRAS, HINDI_MONTHS, HINDI_WEEKDAYS,
    MYTHOLOGY_STORIES,
)


@dataclass
class PanchangContent:
    date_hi: str
    weekday_hi: str
    tithi_hi: str
    nakshatra_hi: str
    paksha_hi: str
    deity_hi: str
    pooja_hi: str
    pooja_slug: str
    hook: str
    cta: str


@dataclass
class RashifalContent:
    rashi: dict
    message_hi: str
    lucky_color_hi: str
    lucky_number: int
    mood_hi: str
    action_hi: str
    pooja_hi: str
    hook: str
    cta: str


@dataclass
class TempleContent:
    temple: dict
    pooja_names: list
    hook: str
    cta: str


@dataclass
class PoojaContent:
    pooja: dict
    hook: str
    cta: str


@dataclass
class NavgrahContent:
    planet: dict
    hook: str
    cta: str


def _seed_rng(target_date: date, salt: str = "") -> random.Random:
    """Deterministic RNG seeded by date + salt for reproducible content."""
    seed = int(target_date.strftime("%Y%m%d")) + hash(salt) % 10000
    return random.Random(seed)


def _format_date_hi(d: date) -> str:
    return f"{d.day} {HINDI_MONTHS[d.month - 1]} {d.year}"


def _pick_hook(hook_type: str, rng: random.Random, **kwargs) -> str:
    templates = HOOKS[hook_type]
    template = rng.choice(templates)
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


def _pick_cta(rng: random.Random) -> str:
    return rng.choice(CTAS)


def _simulate_panchang(d: date, rng: random.Random) -> dict:
    """
    Simulate panchang data using date-based rotation.
    In production, this would call Archana's panchang API or panchangam-js.
    """
    day_of_year = d.timetuple().tm_yday
    lunar_day = (day_of_year * 29 // 365) % 30  # approximate tithi cycle
    nakshatra_idx = (day_of_year * 27 // 365 + d.month) % 27

    tithi_idx = lunar_day % 15
    paksha = "शुक्ल पक्ष" if lunar_day < 15 else "कृष्ण पक्ष"

    return {
        "tithi_hi": TITHIS[tithi_idx],
        "nakshatra_hi": NAKSHATRAS[nakshatra_idx],
        "paksha_hi": paksha,
    }


# Rashifal predictions (curated spiritual messages per rashi)
RASHIFAL_MESSAGES = {
    "mesh": [
        {"msg": "आज का दिन ऊर्जा से भरा है। नए काम शुरू करें, सफलता मिलेगी।", "color": "लाल", "num": 9, "mood": "उत्साही", "action": "सुबह सूर्य को जल चढ़ाएं"},
        {"msg": "धैर्य रखें, किसी से बहस न करें। शाम को मंदिर जाना शुभ रहेगा।", "color": "नारंगी", "num": 3, "mood": "शांत", "action": "हनुमान चालीसा पढ़ें"},
        {"msg": "आर्थिक लाभ के योग हैं। परिवार में खुशी का माहौल रहेगा।", "color": "पीला", "num": 1, "mood": "प्रसन्न", "action": "गणेश जी को मोदक चढ़ाएं"},
    ],
    "vrishabh": [
        {"msg": "आज प्रेम और रिश्तों का दिन है। साथी के साथ समय बिताएं।", "color": "हरा", "num": 6, "mood": "रोमांटिक", "action": "लक्ष्मी पूजा करें"},
        {"msg": "स्वास्थ्य का ध्यान रखें। तला-भुना खाने से बचें।", "color": "सफ़ेद", "num": 2, "mood": "सतर्क", "action": "शिव जी को जल चढ़ाएं"},
        {"msg": "नौकरी में तरक्की के योग हैं। बड़ों का आशीर्वाद लें।", "color": "गुलाबी", "num": 7, "mood": "आशावादी", "action": "सत्यनारायण कथा सुनें"},
    ],
    "mithun": [
        {"msg": "बुद्धि और विवेक से काम लें। पढ़ाई-लिखाई में सफलता मिलेगी।", "color": "हरा", "num": 5, "mood": "बुद्धिमान", "action": "सरस्वती वंदना करें"},
        {"msg": "यात्रा के योग हैं। नए लोगों से मिलना फायदेमंद रहेगा।", "color": "पीला", "num": 3, "mood": "उत्सुक", "action": "गणेश जी की पूजा करें"},
        {"msg": "व्यापार में लाभ होगा। दोपहर बाद कोई अच्छी ख़बर मिल सकती है।", "color": "नीला", "num": 8, "mood": "खुश", "action": "विष्णु सहस्रनाम पढ़ें"},
    ],
    "kark": [
        {"msg": "माता का आशीर्वाद आज विशेष फलदायी है। घर की पूजा करें।", "color": "सफ़ेद", "num": 2, "mood": "भक्तिमय", "action": "दुर्गा माता की आरती करें"},
        {"msg": "भावनाओं पर नियंत्रण रखें। ध्यान और प्राणायाम करें।", "color": "चांदी", "num": 4, "mood": "भावुक", "action": "चंद्र देव को जल चढ़ाएं"},
        {"msg": "संपत्ति संबंधी कार्य शुभ रहेंगे। परिवार में मांगलिक कार्य हो सकता है।", "color": "क्रीम", "num": 9, "mood": "शुभ", "action": "सत्यनारायण कथा करें"},
    ],
    "singh": [
        {"msg": "आज नेतृत्व के गुण चमकेंगे। ऑफिस में सम्मान मिलेगा।", "color": "सोना", "num": 1, "mood": "आत्मविश्वासी", "action": "सूर्य देव को अर्घ्य दें"},
        {"msg": "स्वास्थ्य उत्तम रहेगा। व्यायाम और योग करें।", "color": "लाल", "num": 5, "mood": "ऊर्जावान", "action": "हनुमान जी को सिंदूर चढ़ाएं"},
        {"msg": "रचनात्मक कार्यों में सफलता। कला और संगीत से जुड़ें।", "color": "नारंगी", "num": 3, "mood": "रचनात्मक", "action": "सरस्वती पूजा करें"},
    ],
    "kanya": [
        {"msg": "विश्लेषण शक्ति तेज़ रहेगी। महत्वपूर्ण निर्णय लें।", "color": "हरा", "num": 5, "mood": "विचारशील", "action": "गणेश जी की पूजा करें"},
        {"msg": "स्वास्थ्य का विशेष ध्यान रखें। पेट संबंधी समस्या हो सकती है।", "color": "सफ़ेद", "num": 2, "mood": "सतर्क", "action": "बुध ग्रह शांति करें"},
        {"msg": "पारिवारिक सुख में वृद्धि। बच्चों से अच्छी ख़बर मिलेगी।", "color": "पीला", "num": 7, "mood": "संतुष्ट", "action": "सत्यनारायण कथा सुनें"},
    ],
    "tula": [
        {"msg": "प्रेम और सौंदर्य का दिन। जीवनसाथी के साथ समय बिताएं।", "color": "गुलाबी", "num": 6, "mood": "रोमांटिक", "action": "लक्ष्मी पूजा करें"},
        {"msg": "कानूनी मामलों में सफलता। न्याय आपके पक्ष में होगा।", "color": "नीला", "num": 8, "mood": "शांत", "action": "शनि देव की पूजा करें"},
        {"msg": "व्यापार में नए अवसर आएंगे। साझेदारी शुभ रहेगी।", "color": "हरा", "num": 4, "mood": "व्यावसायिक", "action": "गणेश जी को मोदक चढ़ाएं"},
    ],
    "vrishchik": [
        {"msg": "रहस्यमय ऊर्जा प्रबल है। आध्यात्मिक साधना करें।", "color": "गहरा लाल", "num": 9, "mood": "गहन", "action": "महामृत्युंजय मंत्र जपें"},
        {"msg": "छिपे हुए शत्रुओं से सावधान। हनुमान चालीसा पढ़ें।", "color": "काला", "num": 8, "mood": "सतर्क", "action": "हनुमान जी की पूजा करें"},
        {"msg": "परिवर्तन का समय है। पुराना छोड़ें, नया अपनाएं।", "color": "बैंगनी", "num": 1, "mood": "परिवर्तनशील", "action": "शिव जी का रुद्राभिषेक करें"},
    ],
    "dhanu": [
        {"msg": "भाग्य आज साथ है। लॉटरी या अप्रत्याशित लाभ हो सकता है।", "color": "पीला", "num": 3, "mood": "भाग्यशाली", "action": "गुरुवार का व्रत रखें"},
        {"msg": "धार्मिक यात्रा के योग हैं। तीर्थ स्थान जाना शुभ रहेगा।", "color": "नारंगी", "num": 7, "mood": "धार्मिक", "action": "विष्णु सहस्रनाम पढ़ें"},
        {"msg": "शिक्षा और ज्ञान में उन्नति। गुरु का आशीर्वाद मिलेगा।", "color": "सोना", "num": 5, "mood": "ज्ञानी", "action": "सत्यनारायण कथा करें"},
    ],
    "makar": [
        {"msg": "कड़ी मेहनत का फल मिलेगा। धैर्य बनाए रखें।", "color": "काला", "num": 8, "mood": "मेहनती", "action": "शनि देव को तेल चढ़ाएं"},
        {"msg": "करियर में बड़ी सफलता के संकेत। बॉस से बात करें।", "color": "नीला", "num": 4, "mood": "महत्वाकांक्षी", "action": "शनि चालीसा पढ़ें"},
        {"msg": "स्वास्थ्य पर ध्यान दें। हड्डियों और जोड़ों की देखभाल करें।", "color": "भूरा", "num": 6, "mood": "सतर्क", "action": "हनुमान जी को सिंदूर चढ़ाएं"},
    ],
    "kumbh": [
        {"msg": "नवीन विचार आएंगे। टेक्नोलॉजी से जुड़ा काम शुभ रहेगा।", "color": "नीला", "num": 4, "mood": "नवीन", "action": "शनि देव की पूजा करें"},
        {"msg": "सामाजिक कार्यों में यश मिलेगा। दान-पुण्य करें।", "color": "बैंगनी", "num": 7, "mood": "परोपकारी", "action": "गरीबों को भोजन दान करें"},
        {"msg": "मित्रों से लाभ होगा। पुराने दोस्त से मिलना शुभ।", "color": "आसमानी", "num": 11, "mood": "मैत्रीपूर्ण", "action": "गणेश जी की पूजा करें"},
    ],
    "meen": [
        {"msg": "आध्यात्मिक ऊर्जा प्रबल है। ध्यान और साधना करें।", "color": "सफ़ेद", "num": 7, "mood": "आध्यात्मिक", "action": "विष्णु पूजा करें"},
        {"msg": "कला और संगीत में सफलता। रचनात्मक कार्य करें।", "color": "समुद्री हरा", "num": 3, "mood": "रचनात्मक", "action": "सरस्वती वंदना करें"},
        {"msg": "सपनों में कोई संकेत मिल सकता है। अंतर्मन की सुनें।", "color": "बैंगनी", "num": 9, "mood": "सहज", "action": "गुरु बृहस्पति की पूजा करें"},
    ],
}


@dataclass
class MythologyContent:
    story: dict
    hook: str
    cta: str
    pooja_hi: str


class ContentEngine:
    def get_panchang(self, target_date: Optional[date] = None) -> PanchangContent:
        d = target_date or date.today()
        rng = _seed_rng(d, "panchang")
        panchang = _simulate_panchang(d, rng)
        day_info = DAY_DEITY_MAP[d.weekday()]

        hook = _pick_hook(
            "panchang", rng,
            count=rng.choice([2, 3]),
            tithi=panchang["tithi_hi"],
            nakshatra=panchang["nakshatra_hi"],
            day=day_info["day_hi"],
            deity=day_info["deity_hi"],
        )

        return PanchangContent(
            date_hi=_format_date_hi(d),
            weekday_hi=day_info["day_hi"],
            tithi_hi=panchang["tithi_hi"],
            nakshatra_hi=panchang["nakshatra_hi"],
            paksha_hi=panchang["paksha_hi"],
            deity_hi=day_info["deity_hi"],
            pooja_hi=day_info["pooja_hi"],
            pooja_slug=day_info["pooja"],
            hook=hook,
            cta=_pick_cta(rng),
        )

    def get_rashifal(self, target_date: Optional[date] = None, rashi_slug: Optional[str] = None) -> RashifalContent:
        d = target_date or date.today()
        rng = _seed_rng(d, "rashifal")

        if rashi_slug:
            rashi = next((r for r in RASHIS if r["slug"] == rashi_slug), RASHIS[0])
        else:
            idx = d.timetuple().tm_yday % len(RASHIS)
            rashi = RASHIS[idx]

        messages = RASHIFAL_MESSAGES.get(rashi["slug"], RASHIFAL_MESSAGES["mesh"])
        msg = messages[d.day % len(messages)]

        pooja_map = {
            "mesh": "सूर्य अर्चना", "vrishabh": "लक्ष्मी अर्चना", "mithun": "गणेश अर्चना",
            "kark": "दुर्गा पूजा", "singh": "सूर्य अर्चना", "kanya": "गणेश अर्चना",
            "tula": "लक्ष्मी अर्चना", "vrishchik": "रुद्राभिषेक", "dhanu": "सत्यनारायण कथा",
            "makar": "शनि शांति पूजा", "kumbh": "शनि शांति पूजा", "meen": "सत्यनारायण कथा",
        }

        hook = _pick_hook("rashifal", rng, rashi=rashi["name_hi"])

        return RashifalContent(
            rashi=rashi,
            message_hi=msg["msg"],
            lucky_color_hi=msg["color"],
            lucky_number=msg["num"],
            mood_hi=msg["mood"],
            action_hi=msg["action"],
            pooja_hi=pooja_map.get(rashi["slug"], "गणेश अर्चना"),
            hook=hook,
            cta=_pick_cta(rng),
        )

    def get_temple(self, target_date: Optional[date] = None) -> TempleContent:
        d = target_date or date.today()
        rng = _seed_rng(d, "temple")
        idx = d.timetuple().tm_yday % len(TEMPLES)
        temple = TEMPLES[idx]

        pooja_names = []
        for slug in temple["poojas"]:
            p = next((p for p in POOJAS if p["slug"] == slug), None)
            if p:
                pooja_names.append(p["name_hi"])

        hook = _pick_hook(
            "temple", rng,
            temple=temple["name_hi"],
            city=temple["city_hi"],
        )

        return TempleContent(
            temple=temple,
            pooja_names=pooja_names,
            hook=hook,
            cta=_pick_cta(rng),
        )

    def get_pooja(self, target_date: Optional[date] = None) -> PoojaContent:
        d = target_date or date.today()
        rng = _seed_rng(d, "pooja")
        idx = d.timetuple().tm_yday % len(POOJAS)
        pooja = POOJAS[idx]

        hook = _pick_hook(
            "pooja", rng,
            pooja=pooja["name_hi"],
            deity=pooja["deity_hi"],
        )

        return PoojaContent(pooja=pooja, hook=hook, cta=_pick_cta(rng))

    def get_navgrah(self, target_date: Optional[date] = None) -> NavgrahContent:
        d = target_date or date.today()
        rng = _seed_rng(d, "navgrah")
        idx = d.timetuple().tm_yday % len(NAVGRAH)
        planet = NAVGRAH[idx]

        hook = _pick_hook("navgrah", rng, planet=planet["name_hi"])

        return NavgrahContent(planet=planet, hook=hook, cta=_pick_cta(rng))

    def get_mythology(self, target_date: Optional[date] = None, story_slug: Optional[str] = None) -> MythologyContent:
        d = target_date or date.today()
        rng = _seed_rng(d, "mythology")

        if story_slug:
            story = next((s for s in MYTHOLOGY_STORIES if s["slug"] == story_slug), MYTHOLOGY_STORIES[0])
        else:
            idx = d.timetuple().tm_yday % len(MYTHOLOGY_STORIES)
            story = MYTHOLOGY_STORIES[idx]

        # Find related pooja name
        pooja_hi = ""
        if story.get("related_pooja"):
            p = next((p for p in POOJAS if p["slug"] == story["related_pooja"]), None)
            if p:
                pooja_hi = p["name_hi"]

        return MythologyContent(
            story=story,
            hook=story["hook_hi"],
            cta=rng.choice(SOFT_CTAS),
            pooja_hi=pooja_hi,
        )
