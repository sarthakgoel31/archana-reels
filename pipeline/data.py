"""
Spiritual content data for Archana Reels.
Curated from myarchana.in — temples, poojas, rashis, nakshatras, navgrah, hooks.
"""

# Weekday → Deity → Pooja mapping
DAY_DEITY_MAP = {
    0: {"deity": "surya", "deity_hi": "सूर्य देव", "pooja": "surya-archana", "pooja_hi": "सूर्य अर्चना", "day_hi": "रविवार"},
    1: {"deity": "shiva", "deity_hi": "भगवान शिव", "pooja": "rudrabhishek", "pooja_hi": "रुद्राभिषेक", "day_hi": "सोमवार"},
    2: {"deity": "hanuman", "deity_hi": "हनुमान जी", "pooja": "hanuman-chalisa-path", "pooja_hi": "हनुमान चालीसा पाठ", "day_hi": "मंगलवार"},
    3: {"deity": "ganesh", "deity_hi": "गणेश जी", "pooja": "ganesh-archana", "pooja_hi": "गणेश अर्चना", "day_hi": "बुधवार"},
    4: {"deity": "vishnu", "deity_hi": "भगवान विष्णु", "pooja": "satyanarayan-katha", "pooja_hi": "सत्यनारायण कथा", "day_hi": "गुरुवार"},
    5: {"deity": "lakshmi", "deity_hi": "माता लक्ष्मी", "pooja": "lakshmi-archana", "pooja_hi": "लक्ष्मी अर्चना", "day_hi": "शुक्रवार"},
    6: {"deity": "shani", "deity_hi": "शनि देव", "pooja": "shani-shanti-pooja", "pooja_hi": "शनि शांति पूजा", "day_hi": "शनिवार"},
}

TEMPLES = [
    {
        "name": "Banke Bihari Mandir",
        "name_hi": "बांके बिहारी मंदिर",
        "city": "Vrindavan",
        "city_hi": "वृंदावन",
        "deity": "Krishna",
        "deity_hi": "श्री कृष्ण",
        "hook_fact": "इस मंदिर में भगवान की आँखों में इतनी शक्ति है कि पर्दा लगाना पड़ता है",
        "significance": "भगवान कृष्ण का सबसे प्रसिद्ध मंदिर — यहाँ की मूर्ति तीन जगह से मुड़ी हुई है इसलिए 'बांके' कहलाते हैं",
        "poojas": ["ganesh-archana", "satyanarayan-katha"],
    },
    {
        "name": "Khatu Shyam Ji",
        "name_hi": "खाटू श्याम जी",
        "city": "Sikar, Rajasthan",
        "city_hi": "सीकर, राजस्थान",
        "deity": "Barbarik/Shyam",
        "deity_hi": "श्याम बाबा",
        "hook_fact": "महाभारत का वो योद्धा जो अकेले युद्ध जीत सकता था — आज खाटू श्याम के नाम से पूजे जाते हैं",
        "significance": "भीम के पौत्र बर्बरीक जिन्होंने कृष्ण को अपना शीश दान किया — हारे का साथ देने वाले श्याम बाबा",
        "poojas": ["ganesh-archana", "hanuman-chalisa-path"],
    },
    {
        "name": "Vaishno Devi",
        "name_hi": "वैष्णो देवी",
        "city": "Katra, J&K",
        "city_hi": "कटरा, जम्मू",
        "deity": "Durga",
        "deity_hi": "माता वैष्णो देवी",
        "hook_fact": "14 किलोमीटर की चढ़ाई — लेकिन माता बुलाती हैं तभी जा सकते हो",
        "significance": "त्रिकूट पर्वत पर विराजमान माता — तीन पिंडियों में महाकाली, महालक्ष्मी, महासरस्वती के दर्शन",
        "poojas": ["durga-pooja", "nav-grah-shanti"],
    },
    {
        "name": "Mehandipur Balaji",
        "name_hi": "मेहंदीपुर बालाजी",
        "city": "Dausa, Rajasthan",
        "city_hi": "दौसा, राजस्थान",
        "deity": "Hanuman",
        "deity_hi": "बालाजी महाराज",
        "hook_fact": "ये वो मंदिर है जहाँ लोग बुरी शक्तियों से मुक्ति पाने आते हैं",
        "significance": "संकटमोचन हनुमान जी का सबसे चमत्कारी मंदिर — यहाँ भूत-प्रेत बाधा निवारण होता है",
        "poojas": ["hanuman-chalisa-path", "nav-grah-shanti"],
    },
    {
        "name": "Kashi Vishwanath",
        "name_hi": "काशी विश्वनाथ",
        "city": "Varanasi",
        "city_hi": "वाराणसी",
        "deity": "Shiva",
        "deity_hi": "भगवान शिव",
        "hook_fact": "12 ज्योतिर्लिंगों में सबसे पवित्र — कहते हैं यहाँ मरने से मोक्ष मिलता है",
        "significance": "भगवान शिव की नगरी काशी का सबसे प्राचीन मंदिर — गंगा किनारे विराजमान बाबा विश्वनाथ",
        "poojas": ["rudrabhishek", "nav-grah-shanti"],
    },
    {
        "name": "Tirupati Balaji",
        "name_hi": "तिरुपति बालाजी",
        "city": "Tirupati, AP",
        "city_hi": "तिरुपति, आंध्र प्रदेश",
        "deity": "Vishnu",
        "deity_hi": "भगवान वेंकटेश्वर",
        "hook_fact": "दुनिया का सबसे अमीर मंदिर — रोज़ाना करोड़ों का चढ़ावा आता है",
        "significance": "सात पहाड़ियों पर विराजमान भगवान वेंकटेश्वर — बालाजी के दर्शन से हर मनोकामना पूरी होती है",
        "poojas": ["satyanarayan-katha", "ganesh-archana"],
    },
    {
        "name": "Shirdi Sai Baba",
        "name_hi": "शिरडी साई बाबा",
        "city": "Shirdi, Maharashtra",
        "city_hi": "शिरडी, महाराष्ट्र",
        "deity": "Sai Baba",
        "deity_hi": "साई बाबा",
        "hook_fact": "सबका मालिक एक — ये वो संत हैं जिन्हें हिंदू और मुस्लिम दोनों पूजते हैं",
        "significance": "श्रद्धा और सबूरी के प्रतीक साई बाबा — 'अल्लाह मालिक' कहने वाले फकीर जो भगवान बन गए",
        "poojas": ["satyanarayan-katha", "ganesh-archana"],
    },
    {
        "name": "Siddhivinayak",
        "name_hi": "सिद्धिविनायक",
        "city": "Mumbai",
        "city_hi": "मुंबई",
        "deity": "Ganesh",
        "deity_hi": "गणपति बप्पा",
        "hook_fact": "बॉलीवुड से लेकर बिजनेसमैन तक — मुंबई आए और सिद्धिविनायक नहीं गए तो क्या गए",
        "significance": "मनोकामना पूरी करने वाले गणपति बप्पा — सिद्धि देने वाले विनायक, मुंबई के सबसे प्रसिद्ध मंदिर",
        "poojas": ["ganesh-archana", "satyanarayan-katha"],
    },
    {
        "name": "Sanwariya Seth",
        "name_hi": "सांवरिया सेठ",
        "city": "Chittorgarh, Rajasthan",
        "city_hi": "चित्तौड़गढ़, राजस्थान",
        "deity": "Krishna",
        "deity_hi": "सांवरिया सेठ",
        "hook_fact": "ये मंदिर हर अर्ज़ी सुनता है — कहते हैं सांवरिया सेठ कभी खाली हाथ नहीं लौटाते",
        "significance": "भगवान कृष्ण का 'सेठ' रूप — व्यापारी और भक्त दोनों की हर मनोकामना पूरी करने वाले प्रभु",
        "poojas": ["satyanarayan-katha", "ganesh-archana"],
    },
    {
        "name": "Salasar Balaji",
        "name_hi": "सालासर बालाजी",
        "city": "Churu, Rajasthan",
        "city_hi": "चूरू, राजस्थान",
        "deity": "Hanuman",
        "deity_hi": "बालाजी महाराज",
        "hook_fact": "ये इकलौता हनुमान मंदिर है जहाँ दाढ़ी-मूँछ वाले हनुमान जी हैं",
        "significance": "दाढ़ी-मूँछ वाले हनुमान जी — राजस्थान के सबसे चमत्कारी बालाजी मंदिर",
        "poojas": ["hanuman-chalisa-path", "nav-grah-shanti"],
    },
]

POOJAS = [
    {
        "slug": "surya-archana",
        "name_hi": "सूर्य अर्चना",
        "deity_hi": "सूर्य देव",
        "price": 251,
        "duration": "30 मिनट",
        "description_hi": "सूर्य देव की कृपा से स्वास्थ्य, यश और सफलता प्राप्त होती है",
        "best_days_hi": "रविवार, संक्रांति, रथ सप्तमी",
        "benefits_hi": ["आत्मविश्वास बढ़ता है", "सरकारी कामों में सफलता", "पिता का आशीर्वाद"],
    },
    {
        "slug": "ganesh-archana",
        "name_hi": "गणेश अर्चना",
        "deity_hi": "गणेश जी",
        "price": 251,
        "duration": "30 मिनट",
        "description_hi": "विघ्नहर्ता गणेश जी की पूजा से हर काम की शुरुआत शुभ होती है",
        "best_days_hi": "बुधवार, चतुर्थी, गणेश चतुर्थी",
        "benefits_hi": ["नई शुरुआत में सफलता", "बुद्धि और विवेक", "बाधाओं का नाश"],
    },
    {
        "slug": "hanuman-chalisa-path",
        "name_hi": "हनुमान चालीसा पाठ",
        "deity_hi": "हनुमान जी",
        "price": 351,
        "duration": "45 मिनट",
        "description_hi": "बजरंगबली की चालीसा का पाठ — भय, संकट और बुरी शक्तियों से रक्षा",
        "best_days_hi": "मंगलवार, शनिवार, हनुमान जयंती",
        "benefits_hi": ["भय और संकट से मुक्ति", "शारीरिक बल", "बुरी नज़र से रक्षा"],
    },
    {
        "slug": "shani-shanti-pooja",
        "name_hi": "शनि शांति पूजा",
        "deity_hi": "शनि देव",
        "price": 501,
        "duration": "60 मिनट",
        "description_hi": "शनि की साढ़े साती या ढैय्या चल रही है? शनि शांति पूजा से कष्ट कम होते हैं",
        "best_days_hi": "शनिवार, अमावस्या, शनि जयंती",
        "benefits_hi": ["साढ़ेसाती के कष्ट कम", "न्याय और अनुशासन", "कर्मफल में सुधार"],
    },
    {
        "slug": "rudrabhishek",
        "name_hi": "रुद्राभिषेक",
        "deity_hi": "भगवान शिव",
        "price": 1101,
        "duration": "90 मिनट",
        "description_hi": "शिव जी का सबसे शक्तिशाली अभिषेक — दूध, दही, शहद, गंगाजल से",
        "best_days_hi": "सोमवार, प्रदोष व्रत, महाशिवरात्रि, श्रावण मास",
        "benefits_hi": ["गंभीर रोगों से मुक्ति", "ग्रह दोष निवारण", "मानसिक शांति"],
    },
    {
        "slug": "nav-grah-shanti",
        "name_hi": "नवग्रह शांति पूजा",
        "deity_hi": "नवग्रह",
        "price": 1501,
        "duration": "120 मिनट",
        "description_hi": "सभी 9 ग्रहों की शांति — कुंडली में ग्रह दोष हो तो ये पूजा ज़रूरी है",
        "best_days_hi": "अमावस्या, ग्रहण, संक्रांति",
        "benefits_hi": ["कुंडली दोष निवारण", "सभी ग्रहों की कृपा", "जीवन में स्थिरता"],
    },
    {
        "slug": "satyanarayan-katha",
        "name_hi": "सत्यनारायण कथा",
        "deity_hi": "भगवान विष्णु",
        "price": 751,
        "duration": "90 मिनट",
        "description_hi": "भगवान विष्णु की सबसे फलदायी कथा — पूर्णिमा को करने से विशेष लाभ",
        "best_days_hi": "पूर्णिमा, एकादशी, गुरुवार",
        "benefits_hi": ["परिवार में सुख-शांति", "आर्थिक समृद्धि", "मनोकामना पूर्ति"],
    },
    {
        "slug": "durga-pooja",
        "name_hi": "दुर्गा पूजा",
        "deity_hi": "माता दुर्गा",
        "price": 451,
        "duration": "60 मिनट",
        "description_hi": "शक्ति की देवी माता दुर्गा की पूजा — शत्रु नाश और सुरक्षा के लिए",
        "best_days_hi": "शुक्रवार, अष्टमी, नवरात्रि",
        "benefits_hi": ["शत्रुओं पर विजय", "परिवार की सुरक्षा", "आंतरिक शक्ति"],
    },
]

RASHIS = [
    {"slug": "mesh", "name_hi": "मेष", "name_en": "Aries", "symbol": "\u2648", "planet_hi": "मंगल", "element_hi": "अग्नि"},
    {"slug": "vrishabh", "name_hi": "वृषभ", "name_en": "Taurus", "symbol": "\u2649", "planet_hi": "शुक्र", "element_hi": "पृथ्वी"},
    {"slug": "mithun", "name_hi": "मिथुन", "name_en": "Gemini", "symbol": "\u264a", "planet_hi": "बुध", "element_hi": "वायु"},
    {"slug": "kark", "name_hi": "कर्क", "name_en": "Cancer", "symbol": "\u264b", "planet_hi": "चंद्र", "element_hi": "जल"},
    {"slug": "singh", "name_hi": "सिंह", "name_en": "Leo", "symbol": "\u264c", "planet_hi": "सूर्य", "element_hi": "अग्नि"},
    {"slug": "kanya", "name_hi": "कन्या", "name_en": "Virgo", "symbol": "\u264d", "planet_hi": "बुध", "element_hi": "पृथ्वी"},
    {"slug": "tula", "name_hi": "तुला", "name_en": "Libra", "symbol": "\u264e", "planet_hi": "शुक्र", "element_hi": "वायु"},
    {"slug": "vrishchik", "name_hi": "वृश्चिक", "name_en": "Scorpio", "symbol": "\u264f", "planet_hi": "मंगल", "element_hi": "जल"},
    {"slug": "dhanu", "name_hi": "धनु", "name_en": "Sagittarius", "symbol": "\u2650", "planet_hi": "गुरु", "element_hi": "अग्नि"},
    {"slug": "makar", "name_hi": "मकर", "name_en": "Capricorn", "symbol": "\u2651", "planet_hi": "शनि", "element_hi": "पृथ्वी"},
    {"slug": "kumbh", "name_hi": "कुंभ", "name_en": "Aquarius", "symbol": "\u2652", "planet_hi": "शनि", "element_hi": "वायु"},
    {"slug": "meen", "name_hi": "मीन", "name_en": "Pisces", "symbol": "\u2653", "planet_hi": "गुरु", "element_hi": "जल"},
]

NAVGRAH = [
    {
        "slug": "surya", "name_hi": "सूर्य", "name_en": "Sun",
        "color": "#FFD040", "day_hi": "रविवार",
        "beej_mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "gemstone_hi": "माणिक्य (Ruby)",
        "fact_hi": "सूर्य देव सभी ग्रहों के राजा हैं — इनकी कृपा से आत्मविश्वास और सम्मान मिलता है",
        "remedy_hi": "रविवार को सूर्य को जल चढ़ाएं और आदित्य हृदय स्तोत्र का पाठ करें",
    },
    {
        "slug": "chandra", "name_hi": "चंद्र", "name_en": "Moon",
        "color": "#A0B8D0", "day_hi": "सोमवार",
        "beej_mantra": "ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः",
        "gemstone_hi": "मोती (Pearl)",
        "fact_hi": "चंद्रमा मन के कारक हैं — इनकी कृपा से मानसिक शांति और भावनात्मक संतुलन मिलता है",
        "remedy_hi": "सोमवार का व्रत रखें, शिव जी को जल चढ़ाएं, सफ़ेद वस्तुएं दान करें",
    },
    {
        "slug": "mangal", "name_hi": "मंगल", "name_en": "Mars",
        "color": "#D06040", "day_hi": "मंगलवार",
        "beej_mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "gemstone_hi": "मूंगा (Red Coral)",
        "fact_hi": "मंगल ग्रह साहस और शक्ति के देवता हैं — मांगलिक दोष इन्हीं की वजह से होता है",
        "remedy_hi": "मंगलवार को हनुमान जी की पूजा करें, लाल वस्तुएं दान करें",
    },
    {
        "slug": "budh", "name_hi": "बुध", "name_en": "Mercury",
        "color": "#50B878", "day_hi": "बुधवार",
        "beej_mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "gemstone_hi": "पन्ना (Emerald)",
        "fact_hi": "बुध ग्रह बुद्धि और वाणी के कारक हैं — व्यापार और शिक्षा में सफलता इन्हीं से मिलती है",
        "remedy_hi": "बुधवार को गणेश जी की पूजा करें, हरी मूंग दान करें",
    },
    {
        "slug": "guru", "name_hi": "गुरु (बृहस्पति)", "name_en": "Jupiter",
        "color": "#D4A050", "day_hi": "गुरुवार",
        "beej_mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "gemstone_hi": "पुखराज (Yellow Sapphire)",
        "fact_hi": "गुरु ग्रह ज्ञान, धर्म और संतान के कारक हैं — देवताओं के गुरु बृहस्पति",
        "remedy_hi": "गुरुवार को पीले वस्त्र पहनें, केले का दान करें, विष्णु सहस्रनाम पढ़ें",
    },
    {
        "slug": "shukra", "name_hi": "शुक्र", "name_en": "Venus",
        "color": "#E0A0B8", "day_hi": "शुक्रवार",
        "beej_mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "gemstone_hi": "हीरा (Diamond)",
        "fact_hi": "शुक्र ग्रह प्रेम, सौंदर्य और भौतिक सुखों के कारक हैं — दैत्यों के गुरु शुक्राचार्य",
        "remedy_hi": "शुक्रवार को माता लक्ष्मी की पूजा करें, सफ़ेद मिठाई बांटें",
    },
    {
        "slug": "shani", "name_hi": "शनि", "name_en": "Saturn",
        "color": "#7888A0", "day_hi": "शनिवार",
        "beej_mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
        "gemstone_hi": "नीलम (Blue Sapphire)",
        "fact_hi": "शनि देव न्याय के देवता हैं — साढ़ेसाती और ढैय्या इन्हीं की देन है, लेकिन कर्मफल भी ये ही देते हैं",
        "remedy_hi": "शनिवार को तेल का दीपक जलाएं, काले तिल दान करें, शनि चालीसा पढ़ें",
    },
    {
        "slug": "rahu", "name_hi": "राहु", "name_en": "Rahu",
        "color": "#8888AA", "day_hi": "शनिवार/बुधवार",
        "beej_mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "gemstone_hi": "गोमेद (Hessonite)",
        "fact_hi": "राहु छाया ग्रह हैं — अचानक सफलता या पतन, विदेश यात्रा, और भ्रम इनकी देन है",
        "remedy_hi": "बुधवार को दुर्गा सप्तशती पढ़ें, नारियल जल में प्रवाहित करें",
    },
    {
        "slug": "ketu", "name_hi": "केतु", "name_en": "Ketu",
        "color": "#B8A050", "day_hi": "मंगलवार/शनिवार",
        "beej_mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "gemstone_hi": "लहसुनिया (Cat's Eye)",
        "fact_hi": "केतु मोक्ष और आध्यात्मिक ज्ञान के कारक हैं — संसार से विरक्ति और गहन ज्ञान इनकी देन है",
        "remedy_hi": "गणेश जी की पूजा करें, भैरव बाबा को नारियल चढ़ाएं",
    },
]

TITHIS = [
    "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी",
    "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी",
    "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा/अमावस्या",
]

NAKSHATRAS = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा",
    "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा",
    "पूर्वा फाल्गुनी", "उत्तरा फाल्गुनी", "हस्त", "चित्रा", "स्वाति",
    "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा",
    "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वा भाद्रपद",
    "उत्तरा भाद्रपद", "रेवती",
]

# Hindi month names
HINDI_MONTHS = [
    "जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून",
    "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर",
]

HINDI_WEEKDAYS = ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]

# Hook templates per content type
HOOKS = {
    "panchang": [
        "आज का दिन बहुत खास है — सुनिए क्यों",
        "आज ये {count} काम बिल्कुल मत करो",
        "आज का शुभ मुहूर्त — मिस मत करना",
        "{tithi} को ये एक काम ज़रूर करें",
        "आज {nakshatra} नक्षत्र — जानिए इसका मतलब",
        "आज {day} है — {deity} की कृपा पाने का दिन",
    ],
    "rashifal": [
        "{rashi} वाले ध्यान से सुनें",
        "आज {rashi} राशि के लिए बहुत ज़रूरी संदेश",
        "{rashi} — आज का लकी कलर और नंबर",
        "अगर आपकी राशि {rashi} है तो ये सुनो",
    ],
    "temple": [
        "{temple} का वो राज़ जो कोई नहीं बताता",
        "ये मंदिर हर मन्नत पूरी करता है",
        "{temple} — यहाँ की पूजा की शक्ति अलग है",
        "{city} का ये मंदिर क्यों है इतना चमत्कारी",
    ],
    "pooja": [
        "परेशान हो? ये एक पूजा सब ठीक कर सकती है",
        "{pooja} कब करें और क्यों — जानिए सब कुछ",
        "हफ्ते में एक बार ये पूजा ज़रूर करें",
        "{deity} को प्रसन्न करने का सबसे सही तरीका",
    ],
    "navgrah": [
        "{planet} ग्रह कमज़ोर है? ये करें तुरंत",
        "{planet} — इस ग्रह की शक्ति जानकर हैरान हो जाएंगे",
        "क्या आपकी कुंडली में {planet} दोष है?",
        "{planet} का बीज मंत्र — रोज़ जपें, जीवन बदलें",
    ],
}

CTAS = [
    "अपनी पूजा बुक करें — लिंक इन बायो",
    "असली मंदिर में पूजा करवाएं — myarchana.in",
    "फोटो प्रूफ के साथ पूजा — लिंक इन बायो",
    "आज ही सेवा बुक करें — myarchana.in",
    "घर बैठे मंदिर की पूजा — लिंक इन बायो",
]

# Soft CTAs for non-ad content (mythology, stories)
SOFT_CTAS = [
    "ऐसी और कहानियां सुनने के लिए फॉलो करें",
    "अगर ये कहानी अच्छी लगी तो शेयर ज़रूर करें",
    "कमेंट में बताओ — ये कहानी पहले सुनी थी?",
    "सेव करो और अपने परिवार को भेजो",
    "फॉलो करो — रोज़ नई आध्यात्मिक कहानी",
]

# Mythology stories — high engagement, follower-building content
MYTHOLOGY_STORIES = [
    {
        "slug": "hanuman-leap",
        "title_hi": "हनुमान जी ने समुद्र कैसे पार किया",
        "hook_hi": "100 योजन का समुद्र — और हनुमान जी ने एक ही छलांग में पार कर लिया। ये कहानी सुनकर रोंगटे खड़े हो जाएंगे।",
        "deity": "hanuman",
        "scenes": [
            {
                "text": "राम जी की पूरी वानर सेना समुद्र किनारे खड़ी थी। सामने अथाह समुद्र, और उस पार — लंका, जहां सीता माता बंदी थीं।",
                "image_prompt": "epic wide shot massive monkey army thousands of warriors standing at ocean shore at night huge waves crashing golden Lanka fortress glowing on distant island full moon dramatic clouds ultra detailed mythology concept art 8k cinematic lighting",
            },
            {
                "text": "कोई उपाय नहीं सूझ रहा था। तब जामवंत बोले — हनुमान! तुम्हें अपनी शक्ति का भान नहीं। तुम वो हो जिसने बचपन में सूर्य को निगलने की कोशिश की थी!",
                "image_prompt": "closeup dramatic portrait of mighty Hanuman muscular golden armor glowing eyes realization of divine power orange golden divine aura swirling energy around him mountain cracking beneath his feet epic mythology concept art 8k cinematic",
            },
            {
                "text": "और फिर हनुमान जी ने अपना रूप विशाल किया — इतना विशाल कि पर्वत उनके पैरों तले कांपने लगे, समुद्र की लहरें पीछे हट गईं।",
                "image_prompt": "colossal giant Hanuman towering above mountains growing to enormous size golden divine body glowing ocean waves parting mountain crumbling beneath feet clouds at chest level epic scale mythology concept art 8k cinematic dramatic lighting",
            },
            {
                "text": "एक गर्जना — जय श्री राम — और हनुमान जी ने छलांग लगा दी! हवा चीरते हुए, बादलों को पार करते हुए, समुद्र के ऊपर उड़ चले।",
                "image_prompt": "Hanuman leaping across ocean massive muscular golden body flying through dramatic storm clouds sonic boom shockwave ocean splitting below him divine golden trail behind epic action pose mythology concept art 8k ultra cinematic",
            },
            {
                "text": "लंका पहुंचकर उन्होंने अशोक वाटिका में सीता माता को खोजा। और बोले — माता, राम जी ने भेजा है। वो आ रहे हैं।",
                "image_prompt": "Hanuman kneeling humbly before goddess Sita in beautiful Ashoka garden golden moonlight falling through trees divine emotional devotion tears of joy flowers blooming around them epic mythology concept art 8k cinematic",
            },
        ],
        "moral_hi": "जब तक आपको अपनी शक्ति का भान नहीं — आप सामान्य हैं। भान होते ही, असंभव कुछ भी नहीं। जय बजरंगबली!",
        "related_pooja": "hanuman-chalisa-path",
    },
    {
        "slug": "ganesh-head",
        "title_hi": "गणेश जी का सिर कैसे कटा",
        "hook_hi": "एक पिता ने अपने ही बेटे का सिर काट दिया — और फिर हाथी का सिर लगाया",
        "deity": "ganesh",
        "scenes": [
            {
                "text": "माता पार्वती ने स्नान से पहले चंदन से एक बालक बनाया और उसमें प्राण डाले।",
                "image_prompt": "goddess Parvati creating a boy from sandalwood paste divine golden light ancient Hindu mythology beautiful temple interior cinematic 4k",
            },
            {
                "text": "उन्होंने कहा — द्वार पर खड़े रहो, किसी को अंदर मत आने देना।",
                "image_prompt": "young divine boy standing guard at palace door determined stance ancient Indian palace golden architecture cinematic 4k",
            },
            {
                "text": "भगवान शिव आए, लेकिन बालक ने उन्हें रोक दिया। शिव जी क्रोधित हो गए।",
                "image_prompt": "Lord Shiva confronting young boy at palace entrance divine anger blue skin trishul glowing epic mythology cinematic 4k",
            },
            {
                "text": "क्रोध में शिव जी ने त्रिशूल से बालक का सिर काट दिया। पार्वती ने देखा तो विलाप किया।",
                "image_prompt": "dramatic divine scene aftermath Parvati grieving over child Shiva realizing mistake cosmic background emotional mythology cinematic 4k",
            },
            {
                "text": "शिव जी ने गजराज का सिर लगाकर बालक को पुनर्जीवित किया — और वो बने गणेश, विघ्नहर्ता।",
                "image_prompt": "Lord Ganesh being blessed by Shiva and Parvati elephant head divine golden aura celestial celebration mythology cinematic 4k",
            },
        ],
        "moral_hi": "गणेश जी सिखाते हैं — बाधाएं आती हैं, लेकिन हर बाधा के बाद एक नया रूप मिलता है।",
        "related_pooja": "ganesh-archana",
    },
    {
        "slug": "samudra-manthan",
        "title_hi": "समुद्र मंथन — अमृत कैसे निकला",
        "hook_hi": "देवताओं और असुरों ने मिलकर समुद्र मथा — निकला अमृत, और फिर शुरू हुआ छल",
        "deity": "vishnu",
        "scenes": [
            {
                "text": "दुर्वासा ऋषि के श्राप से देवता कमज़ोर हो गए। विष्णु जी ने कहा — समुद्र मंथन करो, अमृत मिलेगा।",
                "image_prompt": "Lord Vishnu speaking to weakened gods divine blue skin cosmic background ancient mythology advisory scene cinematic 4k",
            },
            {
                "text": "मंदराचल पर्वत को मथनी और वासुकि नाग को रस्सी बनाया। देवता एक तरफ, असुर दूसरी तरफ।",
                "image_prompt": "churning of ocean massive mountain in ocean giant serpent rope gods one side demons other side epic cosmic scale mythology cinematic 4k",
            },
            {
                "text": "सबसे पहले निकला हलाहल विष — इतना भयंकर कि सारी सृष्टि नष्ट हो जाती।",
                "image_prompt": "deadly poison emerging from ocean dark purple deadly smoke gods and demons terrified cosmic danger mythology cinematic 4k",
            },
            {
                "text": "शिव जी ने वो विष पी लिया। गला नीला हो गया — तभी से वो नीलकंठ कहलाए।",
                "image_prompt": "Lord Shiva drinking poison throat turning blue Parvati holding throat divine sacrifice cosmic mythology blue neck Neelkanth cinematic 4k",
            },
            {
                "text": "फिर निकला अमृत। विष्णु जी ने मोहिनी रूप धारण कर अमृत देवताओं को बांट दिया।",
                "image_prompt": "Mohini avatar of Vishnu distributing amrit nectar to gods golden pot divine beauty celestial celebration mythology cinematic 4k",
            },
        ],
        "moral_hi": "हर मंथन में पहले विष निकलता है, फिर अमृत। जीवन में भी — कठिनाई पहले, सफलता बाद में।",
        "related_pooja": "rudrabhishek",
    },
    {
        "slug": "prahlad-holika",
        "title_hi": "प्रह्लाद और होलिका — होली की असली कहानी",
        "hook_hi": "एक पिता ने अपने ही बेटे को जलाने की कोशिश की — लेकिन भगवान ने बचा लिया",
        "deity": "vishnu",
        "scenes": [
            {
                "text": "हिरण्यकश्यपु चाहता था कि सब उसे भगवान मानें। लेकिन उसका बेटा प्रह्लाद विष्णु भक्त था।",
                "image_prompt": "demon king Hiranyakashipu on golden throne angry young boy Prahlad praying peaceful divine contrast mythology cinematic 4k",
            },
            {
                "text": "उसने प्रह्लाद को मारने के कई प्रयास किए — ज़हर दिया, हाथी से कुचलवाया, पहाड़ से गिराया।",
                "image_prompt": "young devotee boy surviving multiple assassination attempts divine protection golden aura shield mythology epic scenes cinematic 4k",
            },
            {
                "text": "आखिर में होलिका को बुलाया — जिसे आग नहीं जला सकती थी। प्रह्लाद को गोद में लेकर आग में बैठी।",
                "image_prompt": "Holika sitting in massive fire with young Prahlad on lap demonic woman flames divine protection mythology dramatic cinematic 4k",
            },
            {
                "text": "लेकिन विष्णु जी की कृपा से होलिका जल गई और प्रह्लाद बच गया। भक्ति जीती, अहंकार हारा।",
                "image_prompt": "Prahlad walking out of fire unharmed divine glow Holika burning victory of devotion mythology golden light cinematic 4k",
            },
            {
                "text": "तभी नरसिंह रूप में विष्णु प्रकट हुए और हिरण्यकश्यपु का वध किया।",
                "image_prompt": "Narasimha avatar half man half lion destroying demon king Hiranyakashipu on doorstep twilight divine fury epic mythology cinematic 4k",
            },
        ],
        "moral_hi": "भक्ति की ताकत सबसे बड़ी है। कोई भी शक्ति सच्चे भक्त का कुछ नहीं बिगाड़ सकती।",
        "related_pooja": "satyanarayan-katha",
    },
    {
        "slug": "shiva-tandav",
        "title_hi": "शिव तांडव — जब शिव ने ब्रह्मांड हिला दिया",
        "hook_hi": "जब शिव जी ने तांडव किया — तो तीनों लोक कांप उठे",
        "deity": "shiva",
        "scenes": [
            {
                "text": "सती के आत्मदाह के बाद शिव जी का हृदय टूट गया। उनके भीतर अपार क्रोध और दुख था।",
                "image_prompt": "Lord Shiva devastated carrying Sati body cosmic grief dark sky storms divine sorrow mythology emotional cinematic 4k",
            },
            {
                "text": "शिव जी ने तांडव शुरू किया। हर कदम से पृथ्वी कांपी, हर थिरकन से तारे टूटे।",
                "image_prompt": "Shiva performing Tandav dance cosmic destruction fire around feet stars falling mountains crumbling divine fury epic mythology cinematic 4k",
            },
            {
                "text": "डमरू की ध्वनि से ब्रह्मांड गूंज उठा। त्रिशूल से आकाश चीरा गया।",
                "image_prompt": "Shiva Nataraja cosmic dance ring of fire damru playing trishul piercing sky destruction and creation mythology cinematic 4k",
            },
            {
                "text": "विष्णु जी ने सुदर्शन चक्र से सती के शरीर के टुकड़े किए — जहां गिरे वहां शक्तिपीठ बनीं।",
                "image_prompt": "51 Shakti Peeths forming across India divine light falling from sky sacred geography temples emerging mythology cinematic 4k",
            },
            {
                "text": "शिव जी शांत हुए, लेकिन उनका तांडव हमें सिखाता है — विनाश से ही सृजन होता है।",
                "image_prompt": "Shiva meditating peacefully on Kailash mountain after Tandav serene cosmic peace new creation beginning mythology cinematic 4k",
            },
        ],
        "moral_hi": "शिव का तांडव सिखाता है — कभी-कभी टूटना ज़रूरी है, ताकि नया बन सके।",
        "related_pooja": "rudrabhishek",
    },
    {
        "slug": "krishna-geeta",
        "title_hi": "गीता का सार — कृष्ण ने अर्जुन को क्या सिखाया",
        "hook_hi": "जब अर्जुन ने हथियार रख दिए — तब कृष्ण ने वो बात कही जो पूरी दुनिया बदल दे",
        "deity": "krishna",
        "scenes": [
            {
                "text": "कुरुक्षेत्र का मैदान। सामने अपने ही परिवार, गुरु, दादा। अर्जुन का मन डोल गया।",
                "image_prompt": "wide shot massive Kurukshetra battlefield two enormous armies facing each other with war elephants horses chariots flags dust clouds dramatic stormy sky epic scale cinematic 4k concept art",
            },
            {
                "text": "कृष्ण ने कहा — तू शोक करता है उनके लिए जो शोक के योग्य नहीं। आत्मा अमर है।",
                "image_prompt": "Lord Krishna with blue skin peacock feather crown yellow silk dhoti speaking wisely to warrior Arjuna who has brown human skin wearing silver battle armor both standing in golden chariot white horses battlefield background divine golden aura cinematic 4k concept art",
            },
            {
                "text": "कर्म करो, फल की चिंता मत करो। ये गीता का सबसे बड़ा संदेश है।",
                "image_prompt": "ancient Sanskrit verses of Bhagavad Gita glowing golden on a cosmic dark background divine wheel chakra of dharma spinning stars and galaxies sacred geometry patterns cinematic 4k concept art",
            },
            {
                "text": "कृष्ण ने अपना विश्वरूप दिखाया — अनंत मुख, अनंत आँखें, पूरा ब्रह्मांड उनके भीतर।",
                "image_prompt": "Krishna Vishwaroop cosmic universal form towering gigantic figure with thousands of faces and arms containing entire universe sun moon galaxies inside his body terrifying and magnificent Arjuna tiny below looking up in awe divine radiance cinematic 4k concept art",
            },
            {
                "text": "अर्जुन समझ गया — कर्म करो, धर्म पर चलो, बाकी कृष्ण पर छोड़ दो।",
                "image_prompt": "warrior Arjuna with brown human skin golden armor standing tall picking up his mighty Gandiva bow with renewed determination sunrise over Kurukshetra battlefield golden light rays Krishna with blue skin smiling behind him cinematic 4k concept art",
            },
        ],
        "moral_hi": "कर्मण्येवाधिकारस्ते — कर्म करो, फल ईश्वर पर छोड़ दो। यही जीवन का सबसे बड़ा सूत्र है।",
        "related_pooja": "satyanarayan-katha",
    },
    {
        "slug": "rahu-ketu-origin",
        "title_hi": "राहु-केतु कैसे बने — छाया ग्रहों की कहानी",
        "hook_hi": "एक असुर ने छल से अमृत पी लिया — विष्णु ने सिर काटा, लेकिन मरा नहीं",
        "deity": "nav_grah",
        "scenes": [
            {
                "text": "समुद्र मंथन से अमृत निकला। विष्णु जी मोहिनी रूप में देवताओं को बांट रहे थे।",
                "image_prompt": "Mohini distributing nectar amrit to gods in line divine beauty golden pot celestial setting mythology cinematic 4k",
            },
            {
                "text": "स्वर्भानु नाम का असुर देवताओं की पंक्ति में छुपकर बैठ गया और अमृत पी लिया।",
                "image_prompt": "demon Svarbhanu disguised among gods secretly drinking nectar amrit sneaky dramatic mythology ancient Indian cinematic 4k",
            },
            {
                "text": "सूर्य और चंद्रमा ने पहचान लिया। विष्णु जी ने तुरंत सुदर्शन चक्र से उसका सिर काट दिया।",
                "image_prompt": "Vishnu throwing Sudarshana Chakra cutting demon in half divine fury cosmic weapon golden disc mythology cinematic 4k",
            },
            {
                "text": "लेकिन अमृत गले तक पहुंच चुका था। सिर राहु बना, धड़ केतु — दोनों अमर हो गए।",
                "image_prompt": "Rahu head and Ketu body becoming two shadow planets cosmic space dark purple eternal immortal mythology cinematic 4k",
            },
            {
                "text": "राहु सूर्य-चंद्र को निगलता है — इसी से ग्रहण होता है। केतु मोक्ष और रहस्य का कारक बना।",
                "image_prompt": "solar eclipse Rahu swallowing sun cosmic phenomenon Ketu spiritual mystical energy shadow planets in space mythology cinematic 4k",
            },
        ],
        "moral_hi": "छल का फल मिलता है — लेकिन कर्म का फल भी। राहु-केतु हमें सिखाते हैं कि हर कर्म का हिसाब होता है।",
        "related_pooja": "nav-grah-shanti",
    },
    {
        "slug": "karna-kavach",
        "title_hi": "कर्ण का कवच-कुंडल दान",
        "hook_hi": "जानते हुए कि मृत्यु निश्चित है — कर्ण ने फिर भी अपना कवच दान कर दिया",
        "deity": "surya",
        "scenes": [
            {
                "text": "कर्ण — सूर्यपुत्र, जन्म से कवच-कुंडल धारी। जब तक कवच था, कोई उसे मार नहीं सकता था।",
                "image_prompt": "warrior Karna with golden divine armor and earrings glowing sun energy Surya son epic warrior mythology Indian cinematic 4k",
            },
            {
                "text": "इंद्र ने ब्राह्मण का वेष धारण किया और कर्ण से उसका कवच-कुंडल मांगा।",
                "image_prompt": "disguised Indra as brahmin asking Karna for donation sunrise golden light dramatic mythology Indian ancient cinematic 4k",
            },
            {
                "text": "सूर्य देव ने चेतावनी दी — दान मत करो, ये तुम्हारी मृत्यु होगी।",
                "image_prompt": "Sun god Surya warning Karna divine father and son moment golden cosmic light concern mythology cinematic 4k",
            },
            {
                "text": "कर्ण ने कहा — दानवीर कर्ण कभी किसी को खाली हाथ नहीं लौटाता। और कवच शरीर से उतारकर दे दिया।",
                "image_prompt": "Karna tearing divine armor from his own body blood sacrifice supreme generosity golden light sacrifice mythology epic cinematic 4k",
            },
            {
                "text": "ये था दानवीर कर्ण — जिसने जानबूझकर मृत्यु चुनी, लेकिन अपना धर्म नहीं छोड़ा।",
                "image_prompt": "Karna standing tall without armor sunset battlefield honor dignity supreme sacrifice mythology golden hour cinematic 4k",
            },
        ],
        "moral_hi": "सच्चा दान वो है जो जानबूझकर कठिन हो। कर्ण ने सिखाया — धर्म जीवन से बड़ा है।",
        "related_pooja": "surya-archana",
    },
    {
        "slug": "durga-mahishasura",
        "title_hi": "दुर्गा vs महिषासुर — शक्ति की जीत",
        "hook_hi": "सभी देवता हार चुके थे — तब एक देवी प्रकट हुईं जिन्होंने अकेले महिषासुर का वध किया",
        "deity": "durga",
        "scenes": [
            {
                "text": "महिषासुर को वरदान मिला था — कोई देवता या मानव उसे मार नहीं सकता। उसने स्वर्ग पर कब्ज़ा कर लिया।",
                "image_prompt": "buffalo demon Mahishasura conquering heaven defeating gods dark powerful demonic army mythology epic battle cinematic 4k",
            },
            {
                "text": "सभी देवताओं के तेज से एक दिव्य नारी शक्ति प्रकट हुई — माता दुर्गा।",
                "image_prompt": "Goddess Durga emerging from combined divine energy of all gods luminous powerful ten arms cosmic creation mythology cinematic 4k",
            },
            {
                "text": "हर देवता ने अपना अस्त्र दिया — शिव ने त्रिशूल, विष्णु ने चक्र, इंद्र ने वज्र।",
                "image_prompt": "gods giving weapons to Durga trishul chakra vajra bow divine weapons glowing each weapon different color mythology cinematic 4k",
            },
            {
                "text": "नौ दिन तक भयंकर युद्ध हुआ। दसवें दिन माता दुर्गा ने महिषासुर का वध किया।",
                "image_prompt": "Durga slaying Mahishasura on lion mount dramatic battle ten arms weapons glowing victory divine feminine power mythology cinematic 4k",
            },
            {
                "text": "इसी विजय को हम नवरात्रि और दशहरा के रूप में मनाते हैं।",
                "image_prompt": "Navratri celebration Durga idol divine victory lights flowers devotees celebrating festival joy mythology cinematic 4k",
            },
        ],
        "moral_hi": "जब सब हार मान लें, तब शक्ति प्रकट होती है। बुराई कितनी भी बड़ी हो — अच्छाई की जीत निश्चित है।",
        "related_pooja": "durga-pooja",
    },
]

# Hooks for mythology content
HOOKS["mythology"] = [
    "ये कहानी सुनकर रोंगटे खड़े हो जाएंगे",
    "ये कहानी हर हिंदू को पता होनी चाहिए",
    "क्या आप जानते हैं ये कहानी?",
    "इस कहानी ने दुनिया बदल दी",
]
