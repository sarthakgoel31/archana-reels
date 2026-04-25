"""
Script writer — generates voiceover text and scene breakdown for each reel type.
Each scene has: type, title_hi, body_hi, duration_sec, bg_style
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Scene:
    scene_type: str       # hook, panchang, info, deity, data, cta
    title_hi: str
    body_hi: str = ""
    subtitle_hi: str = ""
    caption_hi: str = ""   # voiceover subtitle text shown at bottom
    items: list = None     # list of key-value items for data scenes
    duration_sec: float = 4.0
    bg_style: str = "dark"  # dark, light, saffron, deity


@dataclass
class Script:
    voiceover_hi: str
    scenes: list  # list of Scene
    total_duration: float = 0.0

    def __post_init__(self):
        self.total_duration = sum(s.duration_sec for s in self.scenes)


class ScriptWriter:
    def write_panchang(self, content) -> Script:
        scenes = [
            Scene(
                scene_type="hook",
                title_hi=content.hook,
                caption_hi=content.hook,
                duration_sec=3.5,
                bg_style="dark",
            ),
            Scene(
                scene_type="panchang",
                title_hi=f"आज का पंचांग",
                subtitle_hi=content.date_hi,
                caption_hi=f"आज {content.date_hi}, {content.weekday_hi} — तिथि {content.tithi_hi}, नक्षत्र {content.nakshatra_hi}",
                items=[
                    f"दिन: {content.weekday_hi}",
                    f"तिथि: {content.tithi_hi}",
                    f"नक्षत्र: {content.nakshatra_hi}",
                    f"पक्ष: {content.paksha_hi}",
                ],
                duration_sec=6.0,
                bg_style="light",
            ),
            Scene(
                scene_type="deity",
                title_hi=f"आज के देवता",
                body_hi=f"{content.weekday_hi} — {content.deity_hi} का दिन",
                subtitle_hi=f"आज {content.deity_hi} की पूजा करने से विशेष फल मिलता है",
                caption_hi=f"आज {content.deity_hi} का दिन है — पूजा करने से विशेष फल मिलता है",
                duration_sec=5.0,
                bg_style="deity",
            ),
            Scene(
                scene_type="info",
                title_hi=f"आज की पूजा",
                body_hi=content.pooja_hi,
                subtitle_hi=f"असली मंदिर में करवाएं — फोटो प्रूफ के साथ",
                caption_hi=f"{content.pooja_hi} — असली मंदिर में फोटो प्रूफ के साथ बुक करें",
                duration_sec=4.5,
                bg_style="saffron",
            ),
            Scene(
                scene_type="cta",
                title_hi=content.cta,
                subtitle_hi="myarchana.in",
                caption_hi=content.cta,
                duration_sec=3.0,
                bg_style="dark",
            ),
        ]

        voiceover = (
            f"{content.hook}। "
            f"आज {content.date_hi}, {content.weekday_hi} है। "
            f"आज की तिथि है {content.tithi_hi}, {content.paksha_hi}। "
            f"नक्षत्र है {content.nakshatra_hi}। "
            f"आज {content.deity_hi} का दिन है। "
            f"आज {content.deity_hi} की पूजा करने से विशेष फल मिलता है। "
            f"अगर आप {content.pooja_hi} करवाना चाहते हैं, "
            f"तो असली मंदिर में फोटो प्रूफ के साथ पूजा बुक करें। "
            f"{content.cta}।"
        )

        return Script(voiceover_hi=voiceover, scenes=scenes)

    def write_rashifal(self, content) -> Script:
        rashi = content.rashi
        scenes = [
            Scene(
                scene_type="hook",
                title_hi=content.hook,
                caption_hi=content.hook,
                duration_sec=3.0,
                bg_style="dark",
            ),
            Scene(
                scene_type="deity",
                title_hi=f"{rashi['symbol']} {rashi['name_hi']}",
                subtitle_hi=f"{rashi['name_en']} | ग्रह: {rashi['planet_hi']} | तत्व: {rashi['element_hi']}",
                caption_hi=f"{rashi['name_hi']} राशि — ग्रह {rashi['planet_hi']}, तत्व {rashi['element_hi']}",
                duration_sec=3.5,
                bg_style="deity",
            ),
            Scene(
                scene_type="info",
                title_hi="आज का राशिफल",
                body_hi=content.message_hi,
                caption_hi=content.message_hi,
                duration_sec=5.5,
                bg_style="light",
            ),
            Scene(
                scene_type="panchang",
                title_hi="आज का भाग्य",
                caption_hi=f"लकी कलर {content.lucky_color_hi}, नंबर {content.lucky_number} — {content.action_hi}",
                items=[
                    f"लकी कलर: {content.lucky_color_hi}",
                    f"लकी नंबर: {content.lucky_number}",
                    f"मूड: {content.mood_hi}",
                    f"सलाह: {content.action_hi}",
                ],
                duration_sec=5.0,
                bg_style="saffron",
            ),
            Scene(
                scene_type="info",
                title_hi="आज की पूजा",
                body_hi=content.pooja_hi,
                subtitle_hi="मंदिर में पूजा करवाएं — फोटो प्रूफ",
                caption_hi=f"{content.pooja_hi} करवाएं — फोटो प्रूफ के साथ",
                duration_sec=3.5,
                bg_style="saffron",
            ),
            Scene(
                scene_type="cta",
                title_hi=content.cta,
                subtitle_hi="myarchana.in",
                caption_hi=content.cta,
                duration_sec=2.5,
                bg_style="dark",
            ),
        ]

        voiceover = (
            f"{content.hook}। "
            f"आज {rashi['name_hi']} राशि, यानी {rashi['name_en']} के लिए ख़ास संदेश। "
            f"आपका ग्रह है {rashi['planet_hi']}, तत्व है {rashi['element_hi']}। "
            f"{content.message_hi} "
            f"आज का लकी कलर है {content.lucky_color_hi}, "
            f"और लकी नंबर है {content.lucky_number}। "
            f"आज की सलाह: {content.action_hi}। "
            f"अगर आप {content.pooja_hi} करवाना चाहते हैं, "
            f"तो myarchana.in पर जाएं — फोटो प्रूफ के साथ असली मंदिर में पूजा। "
            f"{content.cta}।"
        )

        return Script(voiceover_hi=voiceover, scenes=scenes)

    def write_temple(self, content) -> Script:
        temple = content.temple
        poojas_text = ", ".join(content.pooja_names) if content.pooja_names else "विभिन्न पूजाएं"
        scenes = [
            Scene(
                scene_type="hook",
                title_hi=content.hook,
                caption_hi=content.hook,
                duration_sec=3.5,
                bg_style="dark",
            ),
            Scene(
                scene_type="deity",
                title_hi=temple["name_hi"],
                subtitle_hi=f"{temple['city_hi']} | {temple['deity_hi']}",
                caption_hi=f"{temple['name_hi']}, {temple['city_hi']} — {temple['deity_hi']} विराजमान",
                duration_sec=4.0,
                bg_style="deity",
            ),
            Scene(
                scene_type="info",
                title_hi="मंदिर का महत्व",
                body_hi=temple["significance"],
                caption_hi=temple["significance"][:80],
                duration_sec=7.0,
                bg_style="light",
            ),
            Scene(
                scene_type="panchang",
                title_hi="यहाँ की पूजाएं",
                items=[f"• {name}" for name in content.pooja_names],
                subtitle_hi="घर बैठे बुक करें — प्रसाद डिलीवरी",
                caption_hi=f"{poojas_text} — घर बैठे बुक करें",
                duration_sec=4.5,
                bg_style="saffron",
            ),
            Scene(
                scene_type="cta",
                title_hi=content.cta,
                subtitle_hi="myarchana.in",
                caption_hi=content.cta,
                duration_sec=3.0,
                bg_style="dark",
            ),
        ]

        poojas_text = "। ".join(content.pooja_names) if content.pooja_names else "विभिन्न पूजाएं"

        voiceover = (
            f"{content.hook}। "
            f"आज बात करते हैं {temple['name_hi']} की, "
            f"जो {temple['city_hi']} में स्थित है। "
            f"यहाँ {temple['deity_hi']} विराजमान हैं। "
            f"{temple['significance']}। "
            f"इस मंदिर में {poojas_text} करवा सकते हैं। "
            f"अब घर बैठे असली मंदिर में पूजा बुक करें, "
            f"फोटो प्रूफ और प्रसाद डिलीवरी के साथ। "
            f"{content.cta}।"
        )

        return Script(voiceover_hi=voiceover, scenes=scenes)

    def write_pooja(self, content) -> Script:
        pooja = content.pooja
        scenes = [
            Scene(
                scene_type="hook",
                title_hi=content.hook,
                caption_hi=content.hook,
                duration_sec=3.5,
                bg_style="dark",
            ),
            Scene(
                scene_type="deity",
                title_hi=pooja["name_hi"],
                subtitle_hi=f"{pooja['deity_hi']} | {pooja['duration']} | ₹{pooja['price']}",
                caption_hi=f"{pooja['name_hi']} — {pooja['deity_hi']}, {pooja['duration']}",
                duration_sec=4.0,
                bg_style="deity",
            ),
            Scene(
                scene_type="info",
                title_hi="ये पूजा क्यों करें",
                body_hi=pooja["description_hi"],
                caption_hi=pooja["description_hi"][:80],
                duration_sec=5.0,
                bg_style="light",
            ),
            Scene(
                scene_type="panchang",
                title_hi="पूजा के लाभ",
                caption_hi="। ".join(pooja["benefits_hi"]),
                items=pooja["benefits_hi"],
                duration_sec=5.0,
                bg_style="saffron",
            ),
            Scene(
                scene_type="info",
                title_hi="सबसे शुभ दिन",
                body_hi=pooja["best_days_hi"],
                subtitle_hi=f"₹{pooja['price']} — फोटो प्रूफ गारंटी",
                caption_hi=f"शुभ दिन: {pooja['best_days_hi']} — सिर्फ ₹{pooja['price']}",
                duration_sec=4.0,
                bg_style="saffron",
            ),
            Scene(
                scene_type="cta",
                title_hi=content.cta,
                subtitle_hi="myarchana.in",
                caption_hi=content.cta,
                duration_sec=2.5,
                bg_style="dark",
            ),
        ]

        benefits = "। ".join(pooja["benefits_hi"])

        voiceover = (
            f"{content.hook}। "
            f"आज जानते हैं {pooja['name_hi']} के बारे में। "
            f"ये पूजा {pooja['deity_hi']} को समर्पित है "
            f"और इसकी अवधि है {pooja['duration']}। "
            f"{pooja['description_hi']}। "
            f"इस पूजा के लाभ हैं: {benefits}। "
            f"सबसे शुभ दिन: {pooja['best_days_hi']}। "
            f"सिर्फ {pooja['price']} रुपये में, फोटो प्रूफ गारंटी के साथ। "
            f"{content.cta}।"
        )

        return Script(voiceover_hi=voiceover, scenes=scenes)

    def write_navgrah(self, content) -> Script:
        planet = content.planet
        scenes = [
            Scene(
                scene_type="hook",
                title_hi=content.hook,
                caption_hi=content.hook,
                duration_sec=3.5,
                bg_style="dark",
            ),
            Scene(
                scene_type="deity",
                title_hi=planet["name_hi"],
                subtitle_hi=f"{planet['name_en']} | {planet['day_hi']}",
                caption_hi=f"{planet['name_hi']} — {planet['name_en']}, {planet['day_hi']}",
                duration_sec=3.5,
                bg_style="deity",
            ),
            Scene(
                scene_type="info",
                title_hi="ग्रह का प्रभाव",
                body_hi=planet["fact_hi"],
                caption_hi=planet["fact_hi"][:80],
                duration_sec=6.0,
                bg_style="light",
            ),
            Scene(
                scene_type="panchang",
                title_hi="उपाय",
                items=[
                    f"बीज मंत्र: {planet['beej_mantra']}",
                    f"रत्न: {planet['gemstone_hi']}",
                    f"दिन: {planet['day_hi']}",
                ],
                subtitle_hi=planet["remedy_hi"],
                caption_hi=f"उपाय: {planet['remedy_hi'][:60]}",
                duration_sec=6.0,
                bg_style="saffron",
            ),
            Scene(
                scene_type="cta",
                title_hi=content.hook,
                subtitle_hi="myarchana.in",
                caption_hi=content.cta,
                duration_sec=3.0,
                bg_style="dark",
            ),
        ]

    def write_mythology(self, content) -> Script:
        story = content.story
        story_scenes = story["scenes"]

        scenes = [
            # Hook scene
            Scene(
                scene_type="hook",
                title_hi=story["hook_hi"],
                caption_hi=story["hook_hi"],
                duration_sec=4.0,
                bg_style="dark",
            ),
        ]

        # Story scenes (cinematic — each scene has custom image prompt)
        for i, s in enumerate(story_scenes):
            scenes.append(Scene(
                scene_type="mythology",
                title_hi="",  # no title overlay — let the image speak
                body_hi="",
                caption_hi=s["text"],
                duration_sec=6.0,
                bg_style="dark",
            ))

        # Moral scene
        scenes.append(Scene(
            scene_type="info",
            title_hi="सीख",
            body_hi=story["moral_hi"],
            caption_hi=story["moral_hi"],
            duration_sec=5.0,
            bg_style="deity",
        ))

        # Soft CTA (not salesy)
        scenes.append(Scene(
            scene_type="cta",
            title_hi=content.cta,
            subtitle_hi="myarchana.in" if content.pooja_hi else "",
            caption_hi=content.cta,
            duration_sec=3.0,
            bg_style="dark",
        ))

        # Build voiceover
        narration_parts = [story["hook_hi"] + "।"]
        for s in story_scenes:
            narration_parts.append(s["text"])
        narration_parts.append(story["moral_hi"])
        if content.pooja_hi:
            narration_parts.append(f"अगर आप {content.pooja_hi} करवाना चाहते हैं तो myarchana.in पर जाएं।")
        narration_parts.append(content.cta + "।")

        voiceover = " ".join(narration_parts)

        return Script(voiceover_hi=voiceover, scenes=scenes)
