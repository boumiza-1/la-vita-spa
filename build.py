#!/usr/bin/env python3
"""
Générateur du site La Vita Spa Sousse (FR + AR) — SEO local.
Usage :  python build.py            -> génère le dossier dist/
         SITE_URL=https://mon-domaine.tn python build.py
"""
import html
import json
import os
import shutil
from datetime import date
from pathlib import Path

# ----------------------------------------------------------------------------
# CONFIGURATION — modifiez ici vos informations
# ----------------------------------------------------------------------------
BUSINESS = {
    "name": "La Vita Spa Sousse",
    "phone1": "25213968",          # massage thérapie / hammam turc
    "phone2": "21870211",          # hammam individuel / massage
    "instagram": "https://www.instagram.com/la_vita_spa_sousse/",
    "locality": "Sousse",
    "area": "Sahloul",
    "country": "TN",
    "street": "Sahloul, Sousse",   # remplacez par l'adresse exacte si vous le souhaitez
    "lat": "35.8256",
    "lng": "10.6084",
}
SITE_URL = os.environ.get("SITE_URL", "https://boumiza-1.github.io/la-vita-spa").rstrip("/")
TODAY = date.today().isoformat()
ROOT = Path(__file__).parent
DIST = Path(os.environ["OUT_DIR"]).resolve() if os.environ.get("OUT_DIR") else ROOT  # par défaut : le site est généré dans ce dossier

PH1 = BUSINESS["phone1"]
PH2 = BUSINESS["phone2"]
WA = f"https://wa.me/216{PH1}"

# ----------------------------------------------------------------------------
# DONNÉES : VILLES
# ----------------------------------------------------------------------------
CITIES = {
    "sousse": {
        "fr": "Sousse", "ar": "سوسة",
        "areas_fr": ["Sahloul", "Khezama", "Médina de Sousse", "Port El Kantaoui", "Hammam Sousse", "Chott Meriem", "Akouda", "Kalaa Kebira"],
        "areas_ar": ["سهلول", "خزامة", "مدينة سوسة العتيقة", "ميناء القنطاوي", "حمام سوسة", "شط مريم", "أكودة", "القلعة الكبرى"],
        "intro_fr": "Basé à Sahloul, notre spa vous accueille sur rendez-vous pour des massages thérapeutiques, un hammam turc et des soins du corps. Nous nous déplaçons aussi chez vous dans tout le Grand Sousse.",
        "intro_ar": "مركزنا موجود في سهلول ويستقبلكم بموعد مسبق للماساج العلاجي والحمام التركي والعناية بالجسم. كما نتنقل إلى منزلكم في كامل ولاية سوسة.",
        "local_fr": "Sousse est notre ville : vous pouvez venir au spa de Sahloul (massage, hammam turc, hammam individuel) ou demander un massage à domicile à Khezama, Kantaoui, Hammam Sousse ou en centre-ville.",
        "local_ar": "سوسة هي مدينتنا: يمكنكم القدوم إلى المركز في سهلول (ماساج، حمام تركي، حمام فردي) أو طلب ماساج في المنزل في خزامة أو القنطاوي أو حمام سوسة أو وسط المدينة.",
    },
    "monastir": {
        "fr": "Monastir", "ar": "المنستير",
        "areas_fr": ["Centre-ville de Monastir", "Skanès", "Marina de Monastir", "Ksar Hellal", "Moknine", "Jemmal", "Ouerdanine", "Sayada"],
        "areas_ar": ["وسط المنستير", "سقانص", "مرسى المنستير", "قصر هلال", "المكنين", "جمال", "الوردانين", "صيادة"],
        "intro_fr": "À Monastir, notre masseuse se déplace à votre domicile, à votre hôtel ou dans votre résidence de vacances pour un moment de détente sans stress de transport.",
        "intro_ar": "في المنستير نتنقل إلى منزلكم أو فندقكم أو مقر إقامتكم للعطلة لنمنحكم لحظة استرخاء دون عناء التنقل.",
        "local_fr": "Située à quelques kilomètres de Sousse, Monastir est l'une de nos zones de déplacement les plus demandées, notamment vers Skanès et la zone touristique.",
        "local_ar": "المنستير قريبة من سوسة وهي من أكثر المناطق التي نتنقل إليها، خاصة سقانص والمنطقة السياحية.",
    },
    "nabeul": {
        "fr": "Nabeul", "ar": "نابل",
        "areas_fr": ["Centre-ville de Nabeul", "Dar Chaabane El Fehri", "Beni Khiar", "Mrezga", "Korba", "Kélibia", "Menzel Temime", "Hammam Ghezaz"],
        "areas_ar": ["وسط نابل", "دار شعبان الفهري", "بني خيار", "مرزقة", "قربة", "قليبية", "منزل تميم", "حمام الغزاز"],
        "intro_fr": "Massage à domicile à Nabeul et dans tout le Cap Bon, sur rendez-vous : massage relaxant, massage thérapeutique et hijama à votre domicile.",
        "intro_ar": "ماساج في المنزل بنابل وكامل الوطن القبلي بموعد مسبق: ماساج استرخائي وعلاجي وحجامة عند حضوركم.",
        "local_fr": "Nous nous déplaçons à Nabeul, Dar Chaabane, Beni Khiar, Mrezga et jusqu'à Korba et Kélibia selon la disponibilité. Contactez-nous pour confirmer votre secteur.",
        "local_ar": "نتنقل إلى نابل ودار شعبان وبني خيار ومرزقة وحتى قربة وقليبية حسب التوفر. اتصلوا بنا لتأكيد منطقتكم.",
    },
    "mahdia": {
        "fr": "Mahdia", "ar": "المهدية",
        "areas_fr": ["Centre-ville de Mahdia", "Zone touristique de Mahdia", "Rejiche", "Ksour Essaf", "Chebba", "El Jem", "Bou Merdes", "Salakta"],
        "areas_ar": ["وسط المهدية", "المنطقة السياحية بالمهدية", "الرجيش", "قصور الساف", "الشابة", "الجم", "بومرداس", "سلقطة"],
        "intro_fr": "À Mahdia, profitez d'un massage à domicile professionnel : nous venons chez vous avec notre matériel (huiles, serviettes, outils en bois) pour une séance complète.",
        "intro_ar": "في المهدية نقدم ماساج احترافي في المنزل: نصلكم بكل المعدات (زيوت، مناشف، أدوات خشبية) لحصة كاملة.",
        "local_fr": "Déplacement possible à Mahdia ville, dans la zone touristique, à Rejiche, Ksour Essaf, Chebba et El Jem. Prise de rendez-vous par téléphone ou WhatsApp.",
        "local_ar": "التنقل ممكن إلى مدينة المهدية والمنطقة السياحية والرجيش وقصور الساف والشابة والجم. الحجز عبر الهاتف أو واتساب.",
    },
    "hammamet": {
        "fr": "Hammamet", "ar": "الحمامات",
        "areas_fr": ["Hammamet Nord", "Hammamet Sud", "Yasmine Hammamet", "Centre-ville d'Hammamet", "Mrezka", "Barraket Essahel", "Bir Bouregba"],
        "areas_ar": ["الحمامات الشمالية", "الحمامات الجنوبية", "ياسمين الحمامات", "وسط الحمامات", "مرزقة", "براكة الساحل", "بئر بورقبة"],
        "intro_fr": "À Hammamet, nous venons à votre villa, appartement ou hôtel pour un massage à domicile relaxant ou thérapeutique, ainsi qu'une séance de hijama si vous le souhaitez.",
        "intro_ar": "في الحمامات نصلكم إلى الفيلا أو الشقة أو الفندق لماساج استرخائي أو علاجي في المنزل، وكذلك حجامة عند الطلب.",
        "local_fr": "Hammamet Nord, Hammamet Sud et Yasmine Hammamet font partie de nos zones de déplacement. Réservez à l'avance, surtout en haute saison.",
        "local_ar": "الحمامات الشمالية والجنوبية وياسمين الحمامات ضمن مناطق تنقلنا. احجزوا مسبقًا خاصة في موسم الذروة.",
    },
}

# ----------------------------------------------------------------------------
# DONNÉES : SERVICES
# ----------------------------------------------------------------------------
SERVICES = {
    "massage-a-domicile": {
        "icon": "home_health", "photo": "tools",
        "fr": "Massage à domicile",
        "ar": "ماساج في المنزل",
        "h1_fr": "Massage à domicile à Sousse, Monastir, Nabeul, Mahdia et Hammamet",
        "h1_ar": "ماساج في المنزل بسوسة والمنستير ونابل والمهدية والحمامات",
        "desc_fr": "Massage à domicile en Tunisie : relaxant, thérapeutique, tonique. Nous nous déplaçons chez vous à Sousse, Monastir, Nabeul, Mahdia et Hammamet. Réservation au 25213968.",
        "desc_ar": "ماساج في المنزل بتونس: استرخائي وعلاجي. نتنقل إليكم بسوسة والمنستير ونابل والمهدية والحمامات. للحجز 25213968.",
        "teaser_fr": "On vient chez vous avec tout le matériel : table de massage, huiles, serviettes.",
        "teaser_ar": "نصلكم إلى المنزل بكل المعدات: طاولة ماساج، زيوت، مناشف.",
        "body_fr": [
            ("Un massage chez vous, sans contrainte", "Plus besoin de vous déplacer : nous venons à votre domicile, votre villa ou votre hôtel. Vous restez au calme, vous profitez de la séance puis vous vous reposez directement après. Nous apportons la table de massage, les huiles, les serviettes et les outils de massage en bois."),
            ("Les types de massage proposés", "Massage relaxant aux huiles essentielles, massage thérapeutique (dos, nuque, épaules, jambes), massage tonique, massage aux outils en bois (maderothérapie) et drainage doux. La séance est adaptée à vos besoins : dites-nous simplement où vous avez des tensions."),
            ("Comment réserver", "Appelez le 25213968 ou écrivez-nous sur WhatsApp en indiquant votre ville, votre quartier et le créneau souhaité. Nous confirmons le rendez-vous et l'heure d'arrivée. Le service se fait sur rendez-vous uniquement."),
            ("Zones couvertes", "Sousse (Sahloul, Khezama, Kantaoui, Hammam Sousse), Monastir (Skanès, centre), Nabeul, Mahdia et Hammamet. Pour une autre localité, contactez-nous."),
        ],
        "body_ar": [
            ("ماساج في منزلكم دون عناء", "لا حاجة للتنقل: نصلكم إلى المنزل أو الفيلا أو الفندق. تستمتعون بالحصة في هدوء ثم ترتاحون مباشرة بعدها. نأتي بطاولة الماساج والزيوت والمناشف وأدوات الماساج الخشبية."),
            ("أنواع الماساج", "ماساج استرخائي بالزيوت العطرية، ماساج علاجي (الظهر، الرقبة، الكتفين، الساقين)، ماساج منشط، ماساج بالأدوات الخشبية وتدليك لطيف للتخلص من الاحتقان. نكيّف الحصة حسب حاجتكم: أخبرونا فقط أين تشعرون بالتوتر."),
            ("كيف تحجزون", "اتصلوا على 25213968 أو راسلونا عبر واتساب مع ذكر المدينة والحي والوقت المناسب. نؤكد الموعد ووقت الوصول. الخدمة بموعد مسبق فقط."),
            ("المناطق المغطاة", "سوسة (سهلول، خزامة، القنطاوي، حمام سوسة)، المنستير (سقانص، وسط المدينة)، نابل، المهدية والحمامات. لمنطقة أخرى اتصلوا بنا."),
        ],
        "faq_fr": [
            ("Faites-vous le massage à domicile ?", "Oui. Nous nous déplaçons à Sousse, Monastir, Nabeul, Mahdia et Hammamet sur rendez-vous."),
            ("Que dois-je préparer à la maison ?", "Un espace calme et propre d'environ 2 m sur 2 m. Nous apportons tout le reste."),
            ("Comment prendre rendez-vous ?", "Par téléphone au 25213968 ou par WhatsApp. Indiquez votre ville, votre quartier et l'heure souhaitée."),
        ],
        "faq_ar": [
            ("هل تقدمون ماساج في المنزل؟", "نعم. نتنقل بسوسة والمنستير ونابل والمهدية والحمامات بموعد مسبق."),
            ("ماذا أحضّر في المنزل؟", "مكان هادئ ونظيف بحوالي 2 متر على 2 متر. نحن نحضر كل شيء آخر."),
            ("كيف أحجز موعدًا؟", "عبر الهاتف 25213968 أو واتساب. اذكروا المدينة والحي والوقت المناسب."),
        ],
    },
    "hijama": {
        "icon": "bloodtype", "photo": None,
        "fr": "Hijama (حجامة)",
        "ar": "حجامة",
        "h1_fr": "Hijama (حجامة) à Sousse et à domicile en Tunisie",
        "h1_ar": "حجامة بسوسة وفي المنزل بتونس",
        "desc_fr": "Hijama (حجامة) à Sousse sahloul et à domicile : Monastir, Nabeul, Mahdia, Hammamet. Séance sur rendez-vous au 25213968.",
        "desc_ar": "حجامة بسوسة سهلول وفي المنزل بالمنستير ونابل والمهدية والحمامات. بموعد مسبق على 25213968.",
        "teaser_fr": "Séance de hijama (ventouses) au spa de Sahloul ou à votre domicile.",
        "teaser_ar": "حصة حجامة (كاسات) في المركز بسهلول أو في منزلكم.",
        "body_fr": [
            ("Qu'est-ce que la hijama ?", "La hijama (حجامة) est une pratique traditionnelle de thérapie par ventouses, très répandue dans le monde arabe et musulman. Des ventouses sont posées sur des points précis du dos et du corps. Beaucoup de personnes la pratiquent pour le bien-être et la détente musculaire."),
            ("Au spa ou à domicile", "Vous pouvez venir à Sahloul (Sousse) ou demander une séance à domicile. Le matériel est propre et à usage unique pour les parties en contact avec la peau, et la séance se déroule dans une pièce calme."),
            ("Précautions importantes", "La hijama n'est pas adaptée à tout le monde : grossesse, troubles de la coagulation, traitement anticoagulant, anémie sévère, maladies de peau ou fièvre sont des contre-indications courantes. En cas de problème de santé, demandez l'avis de votre médecin. La hijama ne remplace pas un traitement médical."),
            ("Réservation", "Appelez le 25213968 pour fixer un rendez-vous. Le service est proposé sur rendez-vous à Sousse et à domicile selon la zone."),
        ],
        "body_ar": [
            ("ما هي الحجامة؟", "الحجامة ممارسة تقليدية تعتمد على الكاسات، منتشرة في العالم العربي والإسلامي. توضع الكاسات على نقاط محددة من الظهر والجسم. يلجأ إليها كثيرون من أجل الراحة وارتخاء العضلات."),
            ("في المركز أو في المنزل", "يمكنكم القدوم إلى سهلول (سوسة) أو طلب حصة في المنزل. نحرص على نظافة المعدات واستعمال لوازم لمرة واحدة للأجزاء الملامسة للجلد، والحصة تتم في مكان هادئ."),
            ("احتياطات مهمة", "الحجامة لا تناسب الجميع: الحمل، اضطرابات التخثر، أدوية السيولة، فقر الدم الشديد، الأمراض الجلدية أو الحمى من موانع الاستعمال الشائعة. عند وجود مشكل صحي استشيروا طبيبكم. الحجامة لا تغني عن العلاج الطبي."),
            ("الحجز", "اتصلوا على 25213968 لتحديد موعد. الخدمة بموعد مسبق في سوسة وفي المنزل حسب المنطقة."),
        ],
        "faq_fr": [
            ("La hijama est-elle disponible à domicile ?", "Oui, selon la zone et sur rendez-vous. Contactez-nous au 25213968."),
            ("Y a-t-il des contre-indications ?", "Oui : grossesse, anticoagulants, troubles de la coagulation, anémie sévère, fièvre, maladies de peau. Demandez l'avis de votre médecin en cas de doute."),
        ],
        "faq_ar": [
            ("هل الحجامة متوفرة في المنزل؟", "نعم، حسب المنطقة وبموعد مسبق. اتصلوا على 25213968."),
            ("هل توجد موانع؟", "نعم: الحمل، أدوية السيولة، اضطرابات التخثر، فقر الدم الشديد، الحمى، الأمراض الجلدية. استشيروا طبيبكم عند الشك."),
        ],
    },
    "hammam-sousse-sahloul": {
        "icon": "hot_tub", "photo": "hammam",
        "fr": "Hammam turc à Sahloul",
        "ar": "حمام تركي بسهلول",
        "h1_fr": "Hammam turc et massage thérapie à Sousse Sahloul",
        "h1_ar": "حمام تركي وماساج علاجي بسوسة سهلول",
        "desc_fr": "Hammam turc et thérapie massage sur rendez-vous à Sousse Sahloul. Hammam individuel et massage : 25213968 / 21870211.",
        "desc_ar": "حمام تركي وماساج علاجي بموعد مسبق بسوسة سهلول. حمام فردي وماساج: 25213968 / 21870211.",
        "teaser_fr": "Hammam turc, hammam individuel et massage thérapie à Sahloul, sur rendez-vous.",
        "teaser_ar": "حمام تركي وحمام فردي وماساج علاجي بسهلول بموعد مسبق.",
        "body_fr": [
            ("Notre espace à Sahloul", "Notre spa de Sousse Sahloul propose un hammam turc, un hammam individuel (cabine privée) et des salles de massage thérapie. Tout se fait sur rendez-vous pour garantir calme et intimité."),
            ("Soins disponibles", "Hammam turc traditionnel, gommage, massage thérapie avec huiles et outils en bois, hijama et soins complémentaires. Demandez-nous la formule qui vous convient."),
            ("Réserver au spa", "Pour le hammam turc et le massage thérapie, appelez le 25213968. Pour le hammam individuel, appelez le 21870211. N'oubliez pas d'indiquer le nombre de personnes et l'heure souhaitée."),
            ("Où nous trouver", "Sousse Sahloul. L'adresse exacte vous est communiquée à la confirmation du rendez-vous. Nous suivre : Instagram @la_vita_spa_sousse."),
        ],
        "body_ar": [
            ("مركزنا في سهلول", "يقدم مركزنا بسوسة سهلول حمامًا تركيًا وحمامًا فرديًا (كابينة خاصة) وغرف ماساج علاجي. كل شيء بموعد مسبق لضمان الهدوء والخصوصية."),
            ("الخدمات المتوفرة", "حمام تركي تقليدي، تقشير، ماساج علاجي بالزيوت والأدوات الخشبية، حجامة وعناية تكميلية. اسألونا عن الصيغة المناسبة لكم."),
            ("الحجز في المركز", "للحمام التركي والماساج العلاجي اتصلوا على 25213968. للحمام الفردي اتصلوا على 21870211. اذكروا عدد الأشخاص والوقت المناسب."),
            ("أين تجدوننا", "سوسة سهلول. نعطيكم العنوان الدقيق عند تأكيد الموعد. تابعونا على إنستغرام @la_vita_spa_sousse."),
        ],
        "faq_fr": [
            ("Faut-il réserver pour le hammam ?", "Oui, le hammam turc et le hammam individuel fonctionnent sur rendez-vous."),
            ("Quels numéros appeler ?", "25213968 pour le hammam turc et la thérapie massage ; 21870211 pour le hammam individuel."),
        ],
        "faq_ar": [
            ("هل يجب الحجز للحمام؟", "نعم، الحمام التركي والحمام الفردي بموعد مسبق."),
            ("بأي رقم أتصل؟", "25213968 للحمام التركي والماساج العلاجي، و21870211 للحمام الفردي."),
        ],
    },
}

# ----------------------------------------------------------------------------
# PHOTOS  (fichiers dans assets/images/ — remplacez-les par les vôtres, même nom)
# ----------------------------------------------------------------------------
PHOTOS = {
    "tools":   ("outils-massage.jpg", 714, 830,
                "Outils de massage en bois, huiles et serviettes préparés au spa La Vita à Sousse",
                "أدوات ماساج خشبية وزيوت ومناشف جاهزة في مركز لافيتا سبا بسوسة"),
    "hammam":  ("hammam-turc-sahloul.jpg", 714, 613,
                "Hammam turc traditionnel avec gommage et bougies à Sousse Sahloul",
                "حمام تركي تقليدي مع تقشير وشموع بسوسة سهلول"),
    "hammam2": ("hammam-individuel-sousse.jpg", 622, 572,
                "Hammam individuel avec douche privée à Sousse",
                "حمام فردي بدش خاص بسوسة"),
    "accueil": ("spa-sousse-accueil.jpg", 1000, 933,
                "Accueil au spa La Vita à Sousse Sahloul",
                "الاستقبال في مركز لافيتا سبا بسوسة سهلول"),
    "soins":   ("spa-sousse-soins.jpg", 714, 713,
                "Soins et massage au spa La Vita à Sousse",
                "عناية وماساج في مركز لافيتا سبا بسوسة"),
    "cover": ("https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=1200&q=85", 1200, 1400,
              "Ambiance spa et massage bien-être pour La Vita Spa à Sousse",
              "أجواء سبا وماساج للاسترخاء في لافيتا سبا بسوسة"),
    "massage-photo": ("https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=900&q=85", 900, 900,
              "Ambiance de soins et de bien-être dans un spa",
              "أجواء العناية والاسترخاء في مركز سبا"),
}


ICONS = {
    "home_health": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M12 13v4M10 15h4"/>',
    "bloodtype": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5"/>',
    "hot_tub": '<path d="M3 13h18v2a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M8 3c-1 1.5 1 2.5 0 4M12 3c-1 1.5 1 2.5 0 4M16 3c-1 1.5 1 2.5 0 4"/>',
    "location_on": '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "event_available": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4M9 15l2 2 4-4"/>',
    "spa": '<path d="M12 21c-5 0-8-3.5-8-9 5 0 8 3 8 9z"/><path d="M12 21c5 0 8-3.5 8-9-5 0-8 3-8 9z"/><path d="M12 21c-2-3-2-9 0-13 2 4 2 10 0 13z"/>',
    "call": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
}


def icon(name, cls="svgi"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, ICONS[name]))


def photo(cur, key, lang, lazy=True, cls=""):
    f, w, h, alt_fr, alt_ar = PHOTOS[key]
    alt = alt_ar if lang == "ar" else alt_fr
    src = f if f.startswith("https://") else asset(cur, "images/" + f)
    load = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    klass = ' class="%s"' % cls if cls else ""
    return '<img src="%s" alt="%s" width="%d" height="%d" %s%s data-full="%s">' % (src, e(alt), w, h, load, klass, src)


# ----------------------------------------------------------------------------
# TEXTES UI
# ----------------------------------------------------------------------------
UI = {
    "fr": {
        "lang": "fr", "dir": "ltr", "locale": "fr_TN",
        "home": "Accueil", "services": "Services", "zones": "Zones", "contact": "Contact",
        "call": "Appeler", "whatsapp": "WhatsApp", "book": "Réserver maintenant",
        "other_lang": "العربية",
        "hero_title": "Massage à domicile et spa à Sousse",
        "hero_sub": "Massage relaxant et thérapeutique, hijama et hammam turc. Nous venons chez vous à Sousse, Monastir, Nabeul, Mahdia et Hammamet, ou vous accueillons à Sahloul.",
        "home_title": "Massage à domicile Sousse et Nabeul | Spa, hijama et hammam | La Vita Spa",
        "home_desc": "La Vita Spa Sousse propose massage à domicile à Sousse, Nabeul, Monastir, Mahdia et Hammamet, ainsi que hijama et hammam turc à Sahloul. Contact et rendez-vous WhatsApp : 25213968.",
        "why_title": "Pourquoi nous choisir",
        "why": [("location_on", "À domicile ou au spa", "Vous choisissez : on se déplace chez vous ou vous venez à Sahloul."),
                ("event_available", "Sur rendez-vous", "Un créneau réservé pour vous, dans le calme et l'intimité."),
                ("spa", "Matériel complet", "Huiles, serviettes, table de massage et outils en bois apportés par nos soins."),
                ("call", "Réponse rapide", "Téléphone et WhatsApp pour confirmer votre séance.")],
        "services_title": "Nos services",
        "eyebrow": "Spa & massage · Sousse Sahloul",
        "badge1": "Sur rendez-vous", "badge2": "On se déplace chez vous",
        "marquee": ["Massage à domicile", "Hijama حجامة", "Hammam turc", "Massage thérapie", "Sousse", "Monastir", "Nabeul", "Mahdia", "Hammamet"],
        "steps_title": "Comment ça marche",
        "steps": [("1", "Vous appelez", "Téléphone ou WhatsApp : indiquez votre ville, votre quartier et le service."),
                  ("2", "On confirme", "Nous fixons ensemble le jour, l'heure et l'adresse."),
                  ("3", "Vous vous détendez", "Nous arrivons avec tout le matériel, ou vous venez à Sahloul.")],
        "gallery_title": "Notre matériel, votre bien-être",
        "gallery_text": "Outils de massage en bois, huiles aux essences naturelles, serviettes propres : tout est préparé pour une séance confortable, au spa comme chez vous.",
        "band_title": "Prête pour un moment de détente ?",
        "band_text": "Réservez votre massage à domicile ou votre hammam à Sahloul dès aujourd'hui.",
        "zones_title": "Zones de déplacement",
        "zones_sub": "Cliquez sur votre ville pour voir le détail de notre service de massage à domicile.",
        "local_title": "Notre spa à Sousse Sahloul",
        "local_text": "Hammam turc, hammam individuel et massage thérapie sur rendez-vous, au cœur de Sahloul.",
        "faq_title": "Questions fréquentes",
        "read_more": "En savoir plus",
        "areas_title": "Quartiers et villes couvertes",
        "other_services": "Autres services",
        "other_cities": "Autres villes",
        "contact_title": "Contact et rendez-vous",
        "contact_desc": "Contactez La Vita Spa Sousse : téléphone 25213968 / 21870211, WhatsApp et Instagram. Massage à domicile, hijama, hammam à Sahloul.",
        "contact_h1": "Prenez rendez-vous",
        "contact_p": "Appelez-nous ou écrivez sur WhatsApp en indiquant : votre ville, votre quartier, le service souhaité et l'heure qui vous convient.",
        "phone_lbl1": "Massage thérapie et hammam turc", "phone_lbl2": "Hammam individuel et massage",
        "insta": "Suivez-nous sur Instagram",
        "footer_tag": "Massage à domicile, hijama et hammam turc à Sousse et au Sahel.",
        "rights": "Tous droits réservés.",
        "breadcrumb_home": "Accueil",
        "notfound": "Page introuvable", "notfound_p": "La page demandée n'existe pas.", "back": "Retour à l'accueil",
        "city_h1": "Massage à domicile à {c}",
        "city_title": "Massage à domicile {c} | Massage relaxant et bien-être | La Vita Spa Sousse",
        "city_desc": "Vous cherchez un massage à domicile à {c} ? La Vita Spa Sousse propose des séances de massage relaxant et de bien-être sur rendez-vous. Contactez-nous au 25213968 pour vérifier la disponibilité dans votre quartier.",
        "city_h2_services": "Nos soins à {c}",
        "city_faq": [("Faites-vous le massage à domicile à {c} ?", "Oui, nous nous déplaçons à {c} sur rendez-vous. Appelez le 25213968 ou écrivez sur WhatsApp."),
                     ("Quels soins proposez-vous à {c} ?", "Massage relaxant, massage thérapeutique, massage aux outils en bois et hijama selon disponibilité."),
                     ("Comment réserver à {c} ?", "Indiquez votre quartier et l'horaire souhaité par téléphone ou WhatsApp ; nous confirmons l'heure d'arrivée.")],
    },
    "ar": {
        "lang": "ar", "dir": "rtl", "locale": "ar_TN",
        "home": "الرئيسية", "services": "الخدمات", "zones": "المناطق", "contact": "اتصل بنا",
        "call": "اتصل", "whatsapp": "واتساب", "book": "احجز الآن",
        "other_lang": "Français",
        "hero_title": "ماساج في المنزل وسبا بسوسة",
        "hero_sub": "ماساج استرخائي وعلاجي، حجامة وحمام تركي. نتنقل إليكم بسوسة والمنستير ونابل والمهدية والحمامات، أو نستقبلكم في سهلول.",
        "home_title": "ماساج في المنزل سوسة ونابل | سبا وحجامة وحمام تركي | لافيتا سبا",
        "home_desc": "لافيتا سبا سوسة توفر ماساج في المنزل بسوسة ونابل والمنستير والمهدية والحمامات، مع الحجامة والحمام التركي بسهلول. للحجز والاستفسار عبر الهاتف وواتساب: 25213968.",
        "why_title": "لماذا تختارونا",
        "why": [("location_on", "في المنزل أو في المركز", "أنتم تختارون: نتنقل إليكم أو تأتون إلى سهلول."),
                ("event_available", "بموعد مسبق", "وقت محجوز لكم في هدوء وخصوصية."),
                ("spa", "معدات كاملة", "زيوت ومناشف وطاولة ماساج وأدوات خشبية نأتي بها بأنفسنا."),
                ("call", "رد سريع", "هاتف وواتساب لتأكيد حصتكم.")],
        "services_title": "خدماتنا",
        "eyebrow": "سبا وماساج · سوسة سهلول",
        "badge1": "بموعد مسبق", "badge2": "نتنقل إلى منزلكم",
        "marquee": ["ماساج في المنزل", "حجامة", "حمام تركي", "ماساج علاجي", "سوسة", "المنستير", "نابل", "المهدية", "الحمامات"],
        "steps_title": "كيف تتم الخدمة",
        "steps": [("1", "تتصلون بنا", "هاتف أو واتساب: اذكروا المدينة والحي والخدمة المطلوبة."),
                  ("2", "نؤكد الموعد", "نحدد معكم اليوم والساعة والعنوان."),
                  ("3", "تستمتعون بالراحة", "نصلكم بكل المعدات، أو تأتون إلى سهلول.")],
        "gallery_title": "معداتنا لراحتكم",
        "gallery_text": "أدوات ماساج خشبية، زيوت طبيعية، مناشف نظيفة: كل شيء جاهز لحصة مريحة، في المركز أو في منزلكم.",
        "band_title": "جاهزون للاسترخاء؟",
        "band_text": "احجزوا الماساج في المنزل أو الحمام بسهلول من اليوم.",
        "zones_title": "مناطق التنقل",
        "zones_sub": "اضغطوا على مدينتكم لمعرفة تفاصيل خدمة الماساج في المنزل.",
        "local_title": "مركزنا في سوسة سهلول",
        "local_text": "حمام تركي وحمام فردي وماساج علاجي بموعد مسبق في قلب سهلول.",
        "faq_title": "أسئلة شائعة",
        "read_more": "اعرف المزيد",
        "areas_title": "الأحياء والمدن المغطاة",
        "other_services": "خدمات أخرى",
        "other_cities": "مدن أخرى",
        "contact_title": "اتصل بنا واحجز موعدك",
        "contact_desc": "اتصلوا بلافيتا سبا سوسة: هاتف 25213968 / 21870211، واتساب وإنستغرام. ماساج في المنزل، حجامة، حمام بسهلول.",
        "contact_h1": "احجزوا موعدكم",
        "contact_p": "اتصلوا بنا أو راسلونا على واتساب مع ذكر: المدينة، الحي، الخدمة المطلوبة والوقت المناسب.",
        "phone_lbl1": "ماساج علاجي وحمام تركي", "phone_lbl2": "حمام فردي وماساج",
        "insta": "تابعونا على إنستغرام",
        "footer_tag": "ماساج في المنزل، حجامة وحمام تركي بسوسة والساحل.",
        "rights": "جميع الحقوق محفوظة.",
        "breadcrumb_home": "الرئيسية",
        "notfound": "الصفحة غير موجودة", "notfound_p": "الصفحة المطلوبة غير موجودة.", "back": "العودة إلى الرئيسية",
        "city_h1": "ماساج في المنزل في {c}",
        "city_title": "ماساج في المنزل {c} | ماساج استرخائي وعناية بالجسم | لافيتا سبا سوسة",
        "city_desc": "تبحثون عن ماساج في المنزل في {c}؟ توفر لافيتا سبا سوسة حصص ماساج استرخائي وعناية بالجسم بموعد مسبق. اتصلوا على 25213968 للتأكد من إمكانية التنقل إلى حيّكم.",
        "city_h2_services": "خدماتنا في {c}",
        "city_faq": [("هل تقدمون ماساج في المنزل في {c}؟", "نعم، نتنقل إلى {c} بموعد مسبق. اتصلوا على 25213968 أو راسلونا على واتساب."),
                     ("ما هي الخدمات المتوفرة في {c}؟", "ماساج استرخائي، ماساج علاجي، ماساج بالأدوات الخشبية وحجامة حسب التوفر."),
                     ("كيف أحجز في {c}؟", "اذكروا الحي والوقت المناسب عبر الهاتف أو واتساب وسنؤكد وقت الوصول.")],
    },
}


# ----------------------------------------------------------------------------
# OUTILS
# ----------------------------------------------------------------------------
e = html.escape


def page_path(lang, slug):
    """Chemin relatif du dossier de la page (avec / final)."""
    base = "ar/" if lang == "ar" else ""
    return base + (slug + "/" if slug else "")


def href(from_path, to_path):
    prefix = "../" * from_path.count("/")
    return (prefix + to_path) or "./"


def abs_url(path):
    return f"{SITE_URL}/{path}"


def asset(from_path, name):
    return "../" * from_path.count("/") + "assets/" + name


def nav_html(lang, cur):
    t = UI[lang]
    items = [(t["home"], "")]
    for slug in SERVICES:
        items.append((SERVICES[slug][lang if lang == "ar" else "fr"].split(" (")[0], slug))
    items.append((t["contact"], "contact"))
    out = []
    for label, slug in items:
        link = href(cur, page_path(lang, slug))
        out.append(f'<a href="{link}">{e(label)}</a>')
    return "".join(out)


def schema_business(lang):
    areas = [{"@type": "City", "name": c["fr"]} for c in CITIES.values()]
    return {
        "@context": "https://schema.org",
        "@type": "HealthAndBeautyBusiness",
        "@id": SITE_URL + "/#business",
        "name": BUSINESS["name"],
        "url": SITE_URL + "/",
        "telephone": [f"+216{PH1}", f"+216{PH2}"],
        "sameAs": [BUSINESS["instagram"]],
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BUSINESS["street"],
            "addressLocality": BUSINESS["locality"],
            "addressCountry": BUSINESS["country"],
        },
        "geo": {"@type": "GeoCoordinates", "latitude": BUSINESS["lat"], "longitude": BUSINESS["lng"]},
        "areaServed": areas,
        "knowsAbout": ["Massage à domicile", "Hijama", "Hammam turc", "Massage thérapie", "ماساج", "حجامة"],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Massage à domicile"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Hijama"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Hammam turc"}},
        ],
    }


def schema_faq(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def schema_breadcrumb(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(items)
        ],
    }


def layout(lang, slug, title, desc, body, schemas, noindex=False):
    t = UI[lang]
    cur = page_path(lang, slug)
    other = "fr" if lang == "ar" else "ar"
    fr_path = page_path("fr", slug)
    ar_path = page_path("ar", slug)
    canonical = abs_url(cur)
    alt = ""
    if slug != "404":
        alt = (
            f'<link rel="alternate" hreflang="fr" href="{abs_url(fr_path)}">'
            f'<link rel="alternate" hreflang="ar" href="{abs_url(ar_path)}">'
            f'<link rel="alternate" hreflang="x-default" href="{abs_url(fr_path)}">'
        )
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    ld = "".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas
    )
    switch = href(cur, page_path(other, slug)) if slug != "404" else href(cur, page_path(other, ""))
    fr_cities = "".join(
        f'<a href="{href(cur, page_path(lang, "massage-" + k))}">{e(CITIES[k][lang])}</a>' for k in CITIES
    )
    fr_services = "".join(
        f'<a href="{href(cur, page_path(lang, k))}">{e(SERVICES[k][lang].split(" (")[0])}</a>' for k in SERVICES
    )
    return f"""<!doctype html>
<html lang="{t['lang']}" dir="{t['dir']}" class="no-js">
<head>
<meta charset="utf-8">
<script>document.documentElement.className=""</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
{alt}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:site_name" content="{e(BUSINESS['name'])}">
<meta name="theme-color" content="#7a1f3d">
<meta name="geo.region" content="TN-51">
<meta name="geo.placename" content="Sousse Sahloul">
<link rel="icon" type="image/svg+xml" href="{asset(cur, 'favicon.svg')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset(cur, 'style.css')}">
<script defer src="{asset(cur, 'main.js')}"></script>
{ld}
</head>
<body>
<header class="site-header" id="top">
  <div class="wrap bar">
    <a class="brand" href="{href(cur, page_path(lang, ''))}"><span class="brand-mark">LV</span><span>{e(BUSINESS['name'])}</span></a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false">☰</button>
    <nav class="nav">{nav_html(lang, cur)}<a class="lang" href="{switch}" hreflang="{other}">{e(t['other_lang'])}</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <strong>{e(BUSINESS['name'])}</strong>
      <p>{e(t['footer_tag'])}</p>
      <p><a href="tel:+216{PH1}">{PH1}</a> · <a href="tel:+216{PH2}">{PH2}</a></p>
      <p><a href="{BUSINESS['instagram']}" rel="noopener" target="_blank">Instagram</a> · <a href="{WA}" rel="noopener" target="_blank">WhatsApp</a></p>
    </div>
    <div><strong>{e(t['services'])}</strong><div class="foot-links">{fr_services}</div></div>
    <div><strong>{e(t['zones'])}</strong><div class="foot-links">{fr_cities}</div></div>
  </div>
  <div class="wrap copy">© {date.today().year} {e(BUSINESS['name'])}. {e(t['rights'])}</div>
</footer>
<div class="sticky-cta">
  <a class="btn call" href="tel:+216{PH1}">📞 {e(t['call'])}</a>
  <a class="btn wa" href="{WA}" target="_blank" rel="noopener">💬 {e(t['whatsapp'])}</a>
</div>
</body>
</html>
"""


def faq_html(lang, faqs):
    t = UI[lang]
    items = "".join(
        f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs
    )
    return f'<section class="section"><div class="wrap narrow"><h2>{e(t["faq_title"])}</h2>{items}</div></section>'


def cta_block(lang):
    t = UI[lang]
    return (
        f'<div class="cta-row"><a class="btn call" href="tel:+216{PH1}">📞 {e(t["call"])} {PH1}</a>'
        f'<a class="btn wa" href="{WA}" target="_blank" rel="noopener">💬 {e(t["whatsapp"])}</a></div>'
    )


def service_cards(lang, cur, exclude=None):
    t = UI[lang]
    cards = []
    n = 0
    for k, s_ in SERVICES.items():
        if k == exclude:
            continue
        n += 1
        if s_["photo"]:
            thumb = f'<span class="thumb">{photo(cur, s_["photo"], lang)}<span class="badge-ico">{icon(s_["icon"])}</span></span>'
        else:
            thumb = f'<span class="thumb noimg">{icon(s_["icon"], "svgi big")}</span>'
        cards.append(
            f'<a class="card pic reveal" style="--d:{n * 90}ms" href="{href(cur, page_path(lang, k))}">{thumb}'
            f'<span class="card-body"><h3>{e(s_[lang])}</h3><p>{e(s_["teaser_" + lang])}</p><span class="more">{e(t["read_more"])} →</span></span></a>'
        )
    return "".join(cards)


WAVE = '<svg class="wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0,40 C240,90 480,0 720,30 C960,60 1200,90 1440,35 L1440,80 L0,80 Z"/></svg>'
BLOBS = '<span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span>'


def band_html(lang):
    t = UI[lang]
    return (f'<section class="band"><div class="wrap reveal"><h2>{e(t["band_title"])}</h2><p>{e(t["band_text"])}</p>'
            f'{cta_block(lang)}</div></section>')


def city_cards(lang, cur, exclude=None):
    out = []
    for k, c in CITIES.items():
        if k == exclude:
            continue
        out.append(f'<a class="chip" href="{href(cur, page_path(lang, "massage-" + k))}">📍 {e(c[lang])}</a>')
    return "".join(out)


# ----------------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------------
def build_home(lang):
    t = UI[lang]
    cur = page_path(lang, "")
    why = "".join(
        f'<div class="why reveal" style="--d:{k * 90}ms"><span class="ico">{icon(i)}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>'
        for k, (i, a, b) in enumerate(t["why"])
    )
    steps = "".join(
        f'<div class="step reveal" style="--d:{k * 120}ms"><span class="num">{n}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>'
        for k, (n, a, b) in enumerate(t["steps"])
    )
    mq = "".join(f"<span>{e(x)}</span>" for x in t["marquee"])
    hero_img = photo(cur, "cover", lang, lazy=False)
    gallery = "".join(
        f'<figure class="g g{k} reveal" style="--d:{k * 80}ms">{photo(cur, key, lang)}<figcaption>{e(PHOTOS[key][4 if lang == "ar" else 3].split(" à ")[0].split(" بـ")[0])}</figcaption></figure>'
        for k, key in enumerate(["accueil", "hammam", "tools", "hammam2", "massage-photo"])
    )
    faqs = SERVICES["massage-a-domicile"]["faq_" + lang] + SERVICES["hammam-sousse-sahloul"]["faq_" + lang][:1]
    body = f"""
<section class="hero">
  {BLOBS}
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow">{e(t['eyebrow'])}</span>
      <h1>{e(t['hero_title'])}</h1>
      <p class="lead">{e(t['hero_sub'])}</p>
      {cta_block(lang)}
      <div class="chips">{city_cards(lang, cur)}</div>
    </div>
    <div class="hero-visual">
      <div class="arch">{hero_img}</div>
      <span class="bubble p1">{photo(cur, "accueil", lang, lazy=False)}</span>
      <span class="bubble p2">{photo(cur, "massage-photo", lang, lazy=False)}</span>
      <span class="float f1">🗓️ {e(t['badge1'])}</span>
      <span class="float f2">🏠 {e(t['badge2'])}</span>
      <span class="ring"></span>
    </div>
  </div>
  {WAVE}
</section>
<div class="marquee" aria-hidden="true"><div class="track">{mq}{mq}</div></div>
<section class="section"><div class="wrap"><h2 class="reveal">{e(t['services_title'])}</h2><div class="grid3">{service_cards(lang, cur)}</div></div></section>
<section class="section alt"><div class="wrap">
  <h2 class="reveal">{e(t['gallery_title'])}</h2><p class="reveal">{e(t['gallery_text'])}</p>
  <div class="gallery">{gallery}</div>
  <p class="reveal"><a class="btn ghost" href="{href(cur, page_path(lang, 'hammam-sousse-sahloul'))}">{e(t['local_title'])} →</a></p>
</div></section>

<section class="section testimonials-section" id="avis-clients">
 <div class="wrap">
  <div class="testimonials-heading reveal">
   <span class="eyebrow">{'تجارب حرفائنا' if lang == 'ar' else 'Témoignages clients'}</span>
   <h2>{'آراء حرفائنا' if lang == 'ar' else 'Ils partagent leur expérience'}</h2>
   <p>{'نحبّوا نسمعوا رأيكم وتجربتكم مع لافيتا سبا. نعرضوا هنا آراء حقيقية بعد موافقة أصحابها.' if lang == 'ar' else 'La confiance se construit avec des retours authentiques. Cette galerie est prévue pour accueillir les avis réels de nos clients, publiés avec leur accord.'}</p>
  </div>
  <div class="testimonial-grid">
   <article class="testimonial-card reveal"><div class="testimonial-top"><span class="testimonial-avatar">♥</span><span class="testimonial-stars" aria-label="Emplacement réservé à la note du client">★★★★★</span></div><p>{'نضيفوا هنا نصّ رأي حقيقي من حرفائنا بعد ما ناخذوا موافقتهم.' if lang == 'ar' else 'Ajoutez ici le texte exact d’un avis client authentique, avec son accord.'}</p><div class="testimonial-source">{'رأي حقيقي في انتظار الإضافة' if lang == 'ar' else 'Avis authentique à intégrer'}</div></article>
   <article class="testimonial-card reveal" style="--d:100ms"><div class="testimonial-top"><span class="testimonial-avatar">✦</span><span class="testimonial-stars" aria-label="Emplacement réservé à la note du client">★★★★★</span></div><p>{'يمكنكم إضافة صورة شاشة من فيسبوك أو واتساب بعد إخفاء المعلومات الخاصة.' if lang == 'ar' else 'Vous pouvez intégrer ici une capture d’écran d’un avis Facebook ou WhatsApp, en masquant les données privées.'}</p><div class="testimonial-source">{'صورة رأي بعد الموافقة' if lang == 'ar' else 'Capture d’avis avec autorisation'}</div></article>
   <article class="testimonial-card reveal" style="--d:200ms"><div class="testimonial-top"><span class="testimonial-avatar">✧</span><span class="testimonial-stars" aria-label="Emplacement réservé à la note du client">★★★★★</span></div><p>{'ما نعرضوش أسماء أو تقييمات غير حقيقية؛ كل رأي يتضاف كي يكون عندنا المصدر وموافقة صاحبه.' if lang == 'ar' else 'Chaque témoignage sera ajouté à partir d’un vrai retour client et avec l’autorisation nécessaire.'}</p><div class="testimonial-source">{'تجارب حرفاء حقيقية' if lang == 'ar' else 'Retours vérifiés par votre équipe'}</div></article>
  </div>
  <div class="testimonials-cta"><a class="btn wa" href="{WA}?text={'Je%20souhaite%20partager%20mon%20avis%20sur%20La%20Vita%20Spa' if lang == 'fr' else '%D8%A3%D8%B1%D9%8A%D8%AF%20%D9%85%D8%B4%D8%A7%D8%B1%D9%83%D8%A9%20%D8%B1%D8%A3%D9%8A%D9%8A%20%D8%AD%D9%88%D9%84%20%D9%84%D8%A7%D9%81%D9%8A%D8%AA%D8%A7%20%D8%B3%D8%A8%D8%A7'}" target="_blank" rel="noopener">{'شاركوا رأيكم عبر واتساب' if lang == 'ar' else 'Partager mon avis sur WhatsApp'}</a></div>
 </div>
</section>
<section class="section"><div class="wrap"><h2 class="reveal">{e(t['steps_title'])}</h2><div class="grid3 steps">{steps}</div></div></section>
<section class="section alt"><div class="wrap"><h2 class="reveal">{e(t['why_title'])}</h2><div class="grid4">{why}</div></div></section>
<section class="section"><div class="wrap"><h2 class="reveal">{e(t['zones_title'])}</h2><p class="reveal">{e(t['zones_sub'])}</p><div class="chips big">{city_cards(lang, cur)}</div></div></section>
{faq_html(lang, faqs)}
{band_html(lang)}
"""
    schemas = [schema_business(lang), schema_faq(faqs)]
    return layout(lang, "", t["home_title"], t["home_desc"], body, schemas)


def build_service(lang, key):
    t = UI[lang]
    s = SERVICES[key]
    cur = page_path(lang, key)
    sections = "".join(f"<h2>{e(h)}</h2><p>{e(p)}</p>" for h, p in s["body_" + lang])
    shot = ""
    if s["photo"]:
        extra = photo(cur, "hammam2", lang) if key == "hammam-sousse-sahloul" else ""
        shot = f'<div class="shots reveal"><figure class="shot">{photo(cur, s["photo"], lang)}</figure>{("<figure class=shot>" + extra + "</figure>") if extra else ""}</div>'
    title_suffix = " | La Vita Spa Sousse" if lang == "fr" else " | لافيتا سبا سوسة"
    body = f"""
<section class="page-hero">{BLOBS}<div class="wrap">
  <nav class="crumbs"><a href="{href(cur, page_path(lang, ''))}">{e(t['breadcrumb_home'])}</a> › <span>{e(s[lang])}</span></nav>
  <h1>{e(s['h1_' + lang])}</h1>{cta_block(lang)}
</div>{WAVE}</section>
<section class="section"><div class="wrap narrow prose">{shot}{sections}</div></section>
<section class="section alt"><div class="wrap"><h2>{e(t['zones_title'])}</h2><div class="chips">{city_cards(lang, cur)}</div></div></section>
{faq_html(lang, s['faq_' + lang])}
<section class="section"><div class="wrap"><h2>{e(t['other_services'])}</h2><div class="grid3">{service_cards(lang, cur, exclude=key)}</div></div></section>
{band_html(lang)}
"""
    crumbs = schema_breadcrumb([
        (t["breadcrumb_home"], abs_url(page_path(lang, ""))),
        (s[lang], abs_url(cur)),
    ])
    svc = {
        "@context": "https://schema.org", "@type": "Service",
        "name": s["h1_" + lang], "provider": {"@id": SITE_URL + "/#business"},
        "areaServed": [c["fr"] for c in CITIES.values()], "serviceType": s["fr"],
    }
    return layout(lang, key, s["h1_" + lang] + title_suffix,
                  s["desc_" + lang], body, [schema_business(lang), svc, schema_faq(s["faq_" + lang]), crumbs])


def build_city(lang, key):
    t = UI[lang]
    c = CITIES[key]
    name = c[lang]
    slug = "massage-" + key
    cur = page_path(lang, slug)
    areas = "".join(f"<li>{e(a)}</li>" for a in c["areas_" + lang])
    faqs = [(q.format(c=name), a.format(c=name)) for q, a in t["city_faq"]]
    body = f"""
<section class="page-hero">{BLOBS}<div class="wrap">
  <nav class="crumbs"><a href="{href(cur, page_path(lang, ''))}">{e(t['breadcrumb_home'])}</a> › <span>{e(name)}</span></nav>
  <h1>{e(t['city_h1'].format(c=name))}</h1>
  <p class="lead">{e(c['intro_' + lang])}</p>{cta_block(lang)}
</div>{WAVE}</section>
<section class="section"><div class="wrap narrow prose">
  <p>{e(c['local_' + lang])}</p>
  <h2>{e(t['areas_title'])}</h2><ul class="areas">{areas}</ul>
</div></section>
<section class="section"><div class="wrap"><div class="strip reveal">{photo(cur, "tools", lang)}{photo(cur, "hammam", lang)}{photo(cur, "accueil", lang)}</div></div></section>
<section class="section alt"><div class="wrap"><h2>{e(t['city_h2_services'].format(c=name))}</h2><div class="grid3">{service_cards(lang, cur)}</div></div></section>
{faq_html(lang, faqs)}
<section class="section alt"><div class="wrap"><h2>{e(t['other_cities'])}</h2><div class="chips">{city_cards(lang, cur, exclude=key)}</div></div></section>
{band_html(lang)}
"""
    crumbs = schema_breadcrumb([
        (t["breadcrumb_home"], abs_url(page_path(lang, ""))),
        (name, abs_url(cur)),
    ])
    svc = {
        "@context": "https://schema.org", "@type": "Service",
        "name": t["city_h1"].format(c=name), "provider": {"@id": SITE_URL + "/#business"},
        "areaServed": {"@type": "City", "name": c["fr"]}, "serviceType": "Massage",
    }
    return layout(lang, slug, t["city_title"].format(c=name), t["city_desc"].format(c=name), body,
                  [schema_business(lang), svc, schema_faq(faqs), crumbs])


def build_contact(lang):
    t = UI[lang]
    cur = page_path(lang, "contact")
    maps = "https://www.google.com/maps/search/?api=1&query=" + "spa+massage+Sahloul+Sousse"
    body = f"""
<section class="page-hero">{BLOBS}<div class="wrap">
  <nav class="crumbs"><a href="{href(cur, page_path(lang, ''))}">{e(t['breadcrumb_home'])}</a> › <span>{e(t['contact'])}</span></nav>
  <h1>{e(t['contact_h1'])}</h1><p class="lead">{e(t['contact_p'])}</p>
</div></section>
<section class="section"><div class="wrap grid3">
  <a class="card" href="tel:+216{PH1}"><span class="ico">📞</span><h3>{PH1}</h3><p>{e(t['phone_lbl1'])}</p></a>
  <a class="card" href="tel:+216{PH2}"><span class="ico">📞</span><h3>{PH2}</h3><p>{e(t['phone_lbl2'])}</p></a>
  <a class="card" href="{WA}" target="_blank" rel="noopener"><span class="ico">💬</span><h3>WhatsApp</h3><p>{PH1}</p></a>
  <a class="card" href="{BUSINESS['instagram']}" target="_blank" rel="noopener"><span class="ico">📷</span><h3>Instagram</h3><p>{e(t['insta'])}</p></a>
  <a class="card" href="{maps}" target="_blank" rel="noopener"><span class="ico">📍</span><h3>{e(BUSINESS['street'])}</h3><p>Google Maps</p></a>
</div></section>
<section class="section alt"><div class="wrap"><h2>{e(t['zones_title'])}</h2><div class="chips">{city_cards(lang, cur)}</div></div></section>
"""
    crumbs = schema_breadcrumb([
        (t["breadcrumb_home"], abs_url(page_path(lang, ""))),
        (t["contact"], abs_url(cur)),
    ])
    return layout(lang, "contact", t["contact_title"] + " | La Vita Spa", t["contact_desc"], body,
                  [schema_business(lang), crumbs])


def build_404():
    lang = "fr"
    t = UI[lang]
    cur = "404.html"
    body = f"""<section class="page-hero">{BLOBS}<div class="wrap"><h1>{e(t['notfound'])} / {e(UI['ar']['notfound'])}</h1>
<p class="lead">{e(t['notfound_p'])}</p><p><a class="btn call" href="{SITE_URL}/">{e(t['back'])}</a></p></div></section>"""
    htmldoc = layout(lang, "404", t["notfound"], t["notfound_p"], body, [], noindex=True)
    # la page 404 peut être servie depuis n'importe quel chemin : liens absolus
    return htmldoc.replace('href="../', f'href="{SITE_URL}/').replace('href="./"', f'href="{SITE_URL}/"')


# ----------------------------------------------------------------------------
# SORTIE
# ----------------------------------------------------------------------------
def write(path, content):
    full = DIST / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")


def main():
    if DIST != ROOT:
        if DIST.exists():
            shutil.rmtree(DIST)
        DIST.mkdir(parents=True)
        shutil.copytree(ROOT / "assets", DIST / "assets")
    else:  # génération en place : on ne supprime que les pages générées
        for name in ["ar", "contact", "hijama", "hammam-sousse-sahloul", "massage-a-domicile"] + ["massage-" + k for k in CITIES]:
            shutil.rmtree(ROOT / name, ignore_errors=True)

    urls = []
    for lang in ("fr", "ar"):
        write(page_path(lang, "") + "index.html", build_home(lang))
        urls.append(page_path(lang, ""))
        for key in SERVICES:
            write(page_path(lang, key) + "index.html", build_service(lang, key))
            urls.append(page_path(lang, key))
        for key in CITIES:
            slug = "massage-" + key
            write(page_path(lang, slug) + "index.html", build_city(lang, key))
            urls.append(page_path(lang, slug))
        write(page_path(lang, "contact") + "index.html", build_contact(lang))
        urls.append(page_path(lang, "contact"))

    write("404.html", build_404())

    # sitemap avec hreflang
    def slug_of(p):
        p = p[3:] if p.startswith("ar/") else p
        return p.rstrip("/")

    entries = []
    for p in urls:
        s = slug_of(p)
        fr, ar = abs_url(page_path("fr", s)), abs_url(page_path("ar", s))
        prio = "1.0" if s == "" else ("0.9" if s in SERVICES or s.startswith("massage-") else "0.6")
        entries.append(
            f"<url><loc>{abs_url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority>"
            f'<xhtml:link rel="alternate" hreflang="fr" href="{fr}"/>'
            f'<xhtml:link rel="alternate" hreflang="ar" href="{ar}"/></url>'
        )
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(entries) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"OK : {len(urls)} pages générées dans {DIST} (SITE_URL={SITE_URL})")


if __name__ == "__main__":
    main()
