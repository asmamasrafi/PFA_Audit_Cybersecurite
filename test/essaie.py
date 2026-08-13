"""
Auto-évaluation de la maturité cybersécurité des PME marocaines
CMRPI - Espace Maroc Cyberconfiance | Stage PFA 2026

Page d'accueil "site institutionnel" (inspirée de messervices.cyber.gouv.fr)
+ questionnaire + résultat, en Streamlit.
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Auto-évaluation Cyber PME | CMRPI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =====================================================================
# STYLE
# =====================================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --ink: #12233A;
        --navy-deep: #0D1B2E;
        --teal: #2456A8;
        --teal-deep: #163B72;
        --teal-pale: #E2E9F5;
        --ochre: #C68A3E;
        --ochre-deep: #A5701F;
        --ochre-pale: #F5E9D6;
        --gray: #5B6864;
        --line: #E1E5E2;
        --bg: #FFFFFF;
    }



    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: var(--ink) !important; }

    #MainMenu, header[data-testid="stHeader"], footer {visibility: hidden;}
    .block-container { padding-top: 0 !important; max-width: 100% !important; }
    [data-testid="stSidebar"] { display: none; }

    /* ---------- BARRE DE NAVIGATION ---------- */
    .top-nav {
        display: flex; align-items: center; justify-content: space-between;
        padding: 16px 48px; border-bottom: 1px solid var(--line);
    }
    .top-nav .brand-block { display: flex; align-items: center; gap: 12px; }
    .top-nav .brand-icon {
        width: 42px; height: 42px; border-radius: 50%; background: var(--teal-pale);
        display: flex; align-items: center; justify-content: center; font-size: 20px;
    }
    .top-nav .brand-name { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 17px; color: var(--ink); line-height: 1.1; }
    .top-nav .brand-sub { font-size: 12px; color: var(--gray); }
    .top-nav .nav-links { display: flex; gap: 28px; font-size: 14px; color: var(--ink); font-weight: 500; }
    .top-nav .nav-links span.active { color: var(--teal); border-bottom: 2px solid var(--teal); padding-bottom: 4px; }

    /* ---------- BANDEAU HERO (sombre, façon gouv.fr) ---------- */
    .hero-band {
        background: var(--navy-deep);
        background-image: radial-gradient(circle at 85% 20%, rgba(30,111,99,0.35), transparent 45%);
        padding: 40px 48px 46px 48px;
        color: white;
    }
    .hero-band .breadcrumb { font-size: 12.5px; color: #93A0AC; margin-bottom: 14px; }
    .hero-band h1 { color: white !important; font-size: 34px; margin: 0 0 8px 0; }
    .hero-band p { color: #C7D0D6; font-size: 15px; margin: 0; }

    /* ---------- SECTION PRINCIPALE ---------- */
    .main-pad { padding: 44px 48px 20px 48px; }
    .section-title { font-size: 24px; font-weight: 700; color: var(--ink); margin-bottom: 14px; }
    .section-text { font-size: 15px; color: #3A4750; line-height: 1.65; max-width: 520px; }
    .section-text b { color: var(--ink); }

    /* Bouton principal */
    div.stButton > button[kind="primary"] {
    background-color: #8B1E1E;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 11px 26px;
    font-weight: 700;
    font-size: 15px;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #641515;
    color: white;
}

    div.stButton > button[kind="secondary"] {
        background: white; color: var(--ink); border: 1.5px solid var(--line);
        border-radius: 6px; padding: 9px 20px; font-weight: 500;
    }

    /* Bloc info secondaire */
    .info-block { display: flex; align-items: flex-start; gap: 12px; margin-top: 26px; padding-top: 22px; border-top: 1px solid var(--line); max-width: 520px; }
    .info-block .icon { font-size: 20px; }
    .info-block b { color: var(--ink); font-size: 15.5px; }
    .info-block p { color: var(--gray); font-size: 14px; margin: 4px 0 10px 0; }

    .disclaimer {
        font-style: italic; font-size: 13px; color: var(--gray);
        max-width: 900px; margin-top: 34px; padding-top: 18px; border-top: 1px solid var(--line);
    }

    /* Bande basse */
    .lower-band { background: #F5F7F6; padding: 30px 48px; margin-top: 20px; display: flex; justify-content: space-between; align-items: center; }
    .lower-band h4 { margin: 0 0 6px 0; font-size: 16px; color: var(--ink); }
    .lower-band p { margin: 0; font-size: 13.5px; color: var(--gray); max-width: 500px; }

    footer.custom-footer { padding: 26px 48px; font-size: 12.5px; color: var(--gray); border-top: 1px solid var(--line); }

    /* ---------- CARTE DE QUESTION ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white; border-radius: 14px !important;
        box-shadow: 0 1px 2px rgba(15,27,45,0.04);
    }
    .axe-badge { font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: var(--teal); text-transform: uppercase; margin-bottom: 6px; }
    .q-progress-badge { background: var(--teal-pale); color: var(--teal-deep); font-size: 12.5px; font-weight: 600; padding: 5px 14px; border-radius: 20px; }
    .q-title { font-size: 21px; font-weight: 700; color: var(--ink); margin: 2px 0 18px 0; }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        border: 1.5px solid var(--line); border-radius: 10px; padding: 14px 18px;
        margin-bottom: 10px; width: 100%; transition: border-color 0.15s ease, background 0.15s ease;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover { border-color: var(--teal); background: #FAFCFB; }
    div[data-testid="stRadio"] p { font-size: 15px !important; color: var(--ink) !important; }

    .metric-card { background: white; border: 1px solid var(--line); border-radius: 12px; padding: 20px 22px; }
    .metric-label { font-size: 12.5px; color: var(--gray); text-transform: uppercase; letter-spacing: 0.04em; }
    .metric-value { font-family: 'Space Grotesk', sans-serif; font-size: 30px; font-weight: 700; color: var(--ink); }
    .level-pill { display: inline-block; background: var(--ochre-pale); color: #8A5E24; font-size: 13px; font-weight: 600; padding: 4px 14px; border-radius: 20px; margin-top: 4px; }
    .reco-box { background: white; border: 1px solid var(--line); border-left: 4px solid var(--teal); border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; }
    .reco-theme { font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--teal-deep); font-weight: 700; }
       
        /* =========================================================
       IMAGES DU QUESTIONNAIRE
       ========================================================= */

         /* =========================================================
       IMAGE QUESTIONNAIRE
       ========================================================= */

    div[data-testid="stImage"] {
        width: 100%;
        height: 420px;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        overflow: hidden;
        border-radius: 14px;
        margin-top: 0px;
    }

    div[data-testid="stImage"] img {
        width: 100% !important;
        height: 420px !important;
        object-fit: contain !important;
        object-position: center top !important;
        border-radius: 14px;
        display: block;
    }
    
    </style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =====================================================================
# DONNÉES DU QUESTIONNAIRE
# =====================================================================
AXES = [
    {"nom": "Contexte de l'entreprise", "notee": False, "questions": [
        {"q": "Le système informatique est-il indispensable au fonctionnement quotidien de l'entreprise ?", "opts": ["Non", "Oui"]},
        {"q": "Une panne informatique de plusieurs jours aurait-elle un impact important sur l'activité ?", "opts": ["Non", "Oui"]},
        {"q": "La perte ou la modification accidentelle de données aurait-elle des conséquences importantes ?", "opts": ["Non", "Oui"]},
        {"q": "Une fuite d'informations sensibles (clients, finances) nuirait-elle gravement à l'entreprise ?", "opts": ["Non", "Oui"]},
        {"q": "L'entreprise évolue-t-elle dans un secteur très concurrentiel où l'information a de la valeur ?", "opts": ["Non", "Oui"]},
        {"q": "Le système informatique est-il connecté à internet ou à des partenaires externes ?", "opts": ["Non", "Oui"]},
    ]},
    {"nom": "Gouvernance et organisation", "notee": True, "questions": [
        {"q": "Avez-vous mis en place des règles de sécurité informatique dans votre entreprise ?", "opts": [
            "Aucune règle définie : chacun fait comme il veut.",
            "Quelques règles existent, mais elles sont seulement dites à l'oral et pas toujours suivies.",
            "Des règles sont suivies au quotidien par les employés, mais elles ne sont écrites nulle part.",
            "Il existe un document écrit avec les règles de sécurité, distribué à tous les employés."]},
        {"q": "Une personne est-elle chargée de s'occuper de la sécurité informatique de l'entreprise ?", "opts": [
            "Personne ne s'occupe de la sécurité informatique.",
            "Quelqu'un s'en occupe de temps en temps, sans que ce soit son rôle officiel.",
            "Une personne s'en occupe régulièrement, mais ce n'est pas écrit dans ses fonctions.",
            "Une personne est officiellement désignée responsable, et tout le monde le sait."]},
        {"q": "Savez-vous exactement quels ordinateurs et logiciels sont utilisés dans votre entreprise ?", "opts": [
            "Aucune liste n'existe : personne ne sait précisément ce qui est utilisé.",
            "Une liste existe mais elle est incomplète et rarement mise à jour.",
            "Une liste existe et elle est mise à jour de temps en temps, mais pas systématiquement.",
            "Une liste complète existe et elle est tenue à jour à chaque changement."]},
        {"q": "Réfléchissez-vous régulièrement aux risques informatiques qui menacent votre entreprise (virus, panne, vol) ?", "opts": [
            "Jamais : ces risques ne sont pas évalués.",
            "De temps en temps, mais sans méthode particulière ni suivi.",
            "Régulièrement, en général une fois dans l'année.",
            "Au moins une fois par an, de façon organisée et structurée."]},
    ]},
    {"nom": "Accès, mots de passe et réseau", "notee": True, "questions": [
        {"q": "Chaque employé possède-t-il son propre compte pour se connecter aux ordinateurs et aux logiciels ?", "opts": [
            "Non : plusieurs employés utilisent le même identifiant et le même mot de passe.",
            "Une partie seulement des employés a un compte individuel.",
            "Tous les employés ont un compte individuel.",
            "Tous les employés ont un compte individuel, et l'entreprise vérifie qui accède à quoi."]},
        {"q": "Comment sont gérés les mots de passe dans votre entreprise ?", "opts": [
            "Il n'y a aucune règle particulière sur les mots de passe.",
            "Il existe des règles de base, mais les mots de passe sont rarement changés.",
            "Les mots de passe sont corrects, et changés de temps en temps.",
            "Les mots de passe sont complexes (lettres, chiffres, symboles) et changés régulièrement."]},
        {"q": "Quand un employé quitte l'entreprise, ses accès informatiques sont-ils supprimés ?", "opts": [
            "Non, jamais fait : d'anciens employés peuvent encore avoir accès.",
            "Cela arrive, mais souvent avec du retard.",
            "Cela est fait la plupart du temps.",
            "Cela est fait systématiquement, dès le jour du départ de l'employé."]},
        {"q": "Le réseau Wi-Fi de votre entreprise est-il protégé ?", "opts": [
            "Non, il n'y a pas de mot de passe sur le Wi-Fi.",
            "Il y a un mot de passe, mais il est le même pour les employés et pour les visiteurs.",
            "Il y a un mot de passe, mais il est connu et partagé largement.",
            "Il existe un réseau séparé pour les visiteurs et un réseau protégé pour les employés."]},
        {"q": "Les ordinateurs de votre entreprise sont-ils protégés par un antivirus ?", "opts": [
            "Non, aucun antivirus n'est installé.",
            "Un antivirus est installé sur certains ordinateurs seulement.",
            "Un antivirus est installé partout, mais il n'est pas toujours mis à jour.",
            "Un antivirus est installé et mis à jour sur tous les ordinateurs."]},
    ]},
    {"nom": "Sensibilisation et sécurité humaine", "notee": True, "questions": [
        {"q": "Vos employés sont-ils informés des risques liés à internet et aux emails (virus, arnaques) ?", "opts": [
            "Non, aucune information n'est donnée à ce sujet.",
            "Quelques conseils sont donnés de temps en temps, de manière informelle.",
            "Une information est donnée de temps en temps, mais sans régularité.",
            "Une formation ou une information est organisée au moins une fois par an."]},
        {"q": "Vos employés savent-ils reconnaître un email suspect ou une tentative d'arnaque (phishing) ?", "opts": [
            "Non, les employés ne sont pas informés sur ce sujet.",
            "Quelques employés seulement savent reconnaître un email suspect.",
            "La plupart des employés savent le reconnaître.",
            "Tous les employés savent reconnaître un email suspect et savent quoi faire."]},
        {"q": "L'accès aux locaux où se trouvent les ordinateurs et serveurs importants est-il protégé ?", "opts": [
            "Non, aucune protection particulière (portes ouvertes, accès libre).",
            "Quelques précautions de bon sens sont prises, mais rien d'organisé.",
            "L'accès à certaines zones sensibles est limité.",
            "L'accès est strictement contrôlé, par exemple avec une porte fermée à clé ou un badge."]},
        {"q": "Les informations confidentielles (données des clients, dossiers du personnel) sont-elles protégées ?", "opts": [
            "Non, aucune protection particulière n'est mise en place.",
            "L'accès est limité, mais de façon informelle, sans règle précise.",
            "L'accès est restreint, mais ce n'est pas écrit officiellement.",
            "L'accès est restreint et protégé, par exemple par un mot de passe ou un dossier réservé."]},
    ]},
    {"nom": "Sauvegarde, incidents et conformité", "notee": True, "questions": [
        {"q": "Les données importantes de votre entreprise (factures, clients, documents) sont-elles sauvegardées ?", "opts": [
            "Non, il n'y a aucune sauvegarde.",
            "Une sauvegarde est faite de temps en temps, sans planification.",
            "Une sauvegarde est faite régulièrement, mais elle n'est jamais vérifiée.",
            "Une sauvegarde est faite régulièrement et son bon fonctionnement est vérifié."]},
        {"q": "Où sont conservées les sauvegardes de vos données ?", "opts": [
            "Toujours au même endroit que les données d'origine (même ordinateur ou serveur).",
            "Une copie est faite ailleurs, mais seulement de temps en temps.",
            "Une copie est faite ailleurs régulièrement.",
            "Les sauvegardes sont toujours conservées ailleurs (disque externe ou cloud)."]},
        {"q": "En cas de problème informatique (panne, piratage), vos employés savent-ils quoi faire ?", "opts": [
            "Non, il n'existe aucune consigne à ce sujet.",
            "On réagit au cas par cas, sans règle précise.",
            "Certaines consignes existent et sont connues de quelques personnes seulement.",
            "Il existe une procédure écrite, connue de tous les employés."]},
        {"q": "Si votre système informatique tombait en panne pendant plusieurs jours, votre entreprise pourrait-elle continuer à fonctionner ?", "opts": [
            "Non, aucun plan n'est prévu pour ce genre de situation.",
            "Quelques solutions de secours existent, mais de façon ponctuelle.",
            "Un plan existe, mais il n'est pas complet ni testé.",
            "Un plan complet existe et a déjà été testé pour vérifier qu'il fonctionne."]},
        {"q": "Votre entreprise respecte-t-elle les règles marocaines sur la protection des données personnelles (loi 09-08) ?", "opts": [
            "Non, ces règles ne sont pas respectées.",
            "Elles sont respectées de façon isolée, sans démarche organisée.",
            "Elles sont généralement respectées.",
            "Elles sont respectées et l'entreprise vérifie régulièrement qu'elle est en conformité."]},
    ]},
]

QUESTIONS_FLAT = []
for axe in AXES:
    for q in axe["questions"]:
        QUESTIONS_FLAT.append({"axe": axe["nom"], "notee": axe["notee"], **q})

TOTAL_QUESTIONS = len(QUESTIONS_FLAT)
INDICES_NOTEES = [i for i, q in enumerate(QUESTIONS_FLAT) if q["notee"]]
SCORE_MAX = len(INDICES_NOTEES) * 3

RECOMMANDATIONS = {
    6: "Rédigez un document simple listant les règles de sécurité de base et partagez-le avec tous les employés.",
    7: "Désignez une personne responsable de la sécurité informatique, même à temps partiel.",
    8: "Faites l'inventaire de tout votre matériel et vos logiciels, et tenez-le à jour.",
    9: "Prenez le temps, une fois par an, d'évaluer les risques informatiques de l'entreprise.",
    10: "Donnez à chaque employé un compte individuel : évitez les comptes partagés.",
    11: "Mettez en place des règles claires sur les mots de passe (complexité, renouvellement régulier).",
    12: "Retirez systématiquement les accès informatiques d'un employé dès son départ.",
    13: "Séparez le réseau Wi-Fi des visiteurs de celui des employés, et protégez les deux par un mot de passe.",
    14: "Installez un antivirus à jour sur tous les postes de travail.",
    15: "Organisez une session annuelle de sensibilisation aux risques informatiques.",
    16: "Formez vos employés à reconnaître les emails suspects et les tentatives de phishing.",
    17: "Contrôlez l'accès physique aux locaux où se trouvent vos ordinateurs et serveurs.",
    18: "Restreignez l'accès aux données confidentielles (clients, RH) à un nombre limité de personnes.",
    19: "Mettez en place une sauvegarde régulière de vos données importantes.",
    20: "Conservez une copie de vos sauvegardes ailleurs que sur le poste ou serveur principal.",
    21: "Rédigez une procédure simple expliquant quoi faire en cas d'incident informatique.",
    22: "Préparez un plan de secours pour continuer à fonctionner en cas de panne majeure.",
    23: "Vérifiez que votre entreprise respecte la loi 09-08 sur la protection des données personnelles.",
}

NIVEAUX = [(0.25, "Niveau 1 — Initial"), (0.50, "Niveau 2 — Basique"),
           (0.75, "Niveau 3 — Intermédiaire"), (1.01, "Niveau 4 — Avancé")]


def niveau_maturite(score, score_max):
    ratio = score / score_max if score_max else 0
    for seuil, nom in NIVEAUX:
        if ratio <= seuil:
            return nom
    return NIVEAUX[-1][1]


# =====================================================================
# ÉTAT
# =====================================================================
defaults = {"page": "accueil", "question_courante": 0, "reponses": {}, "historique": []}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def aller_a(page):
    st.session_state.page = page
    st.rerun()


def demarrer_test():
    st.session_state.question_courante = 0
    st.session_state.reponses = {}
    aller_a("questionnaire")


# =====================================================================
# EN-TÊTE COMMUN (barre de nav, toutes pages)
# =====================================================================
def barre_navigation():
    st.markdown(
        """
        <div class="top-nav">
            <div class="brand-block">
                <div class="brand-icon">🛡️</div>
                <div>
                    <div class="brand-name">CyberAudit PME</div>
                    <div class="brand-sub">CMRPI · Espace Maroc Cyberconfiance</div>
                </div>
            </div>
            <div class="nav-links">
                <span class="active">Test de maturité</span>
                <span>Guide CMRPI/AUSIM</span>
                <span>À propos</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bandeau_hero(fil_ariane_extra=None):
    fil = "Accueil &nbsp;›&nbsp; Test de maturité cyber"
    if fil_ariane_extra:
        fil += f" &nbsp;›&nbsp; {fil_ariane_extra}"
    st.markdown(
        f"""
        <div class="hero-band">
            <div class="breadcrumb">{fil}</div>
            <h1>Test de maturité cyber</h1>
            <p>Obtenez en 5 minutes une évaluation indicative de la maturité cybersécurité de votre PME.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chemin_image_axe(numero_axe):
    # Dictionnaire reliant chaque numéro d'axe au nom de son image
    images_axes = {
        0: "images/image2.png",
        1: "images/image5.png",
        2: "images/image1.png",
        3: "images/image4.png",
        4: "images/image3.png",
    }
    # Si le numéro d'axe existe, on retourne le chemin, sinon une image par défaut
    return images_axes.get(numero_axe, "images/votre_image.png")

# =====================================================================
# PAGE — ACCUEIL
# =====================================================================
def page_accueil():
    barre_navigation()
    bandeau_hero()


    

    st.markdown('<div class="main-pad">', unsafe_allow_html=True)
    col_texte, col_image = st.columns([1.1, 1], gap="large")

    with col_texte:
        st.markdown('<div class="section-title">Quelle est la maturité cyber de votre PME ?</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="section-text">
            La maturité cyber reflète le niveau global de prise en compte des enjeux de cybersécurité
            par votre entreprise. Répondez à <b>{TOTAL_QUESTIONS} questions</b>, basées sur le
            <b>Guide de bonnes pratiques CMRPI/AUSIM</b>, pour obtenir votre évaluation indicative.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Débuter le test", type="primary"):
            demarrer_test()

        st.markdown(
            """
            <div class="info-block">
                <div class="icon">📖</div>
                <div>
                    <b>Basé sur le guide CMRPI/AUSIM</b>
                    <p>Ce test reprend les thèmes du Guide de bonnes pratiques cybersécurité pour les
                    PME marocaines, sans jargon technique.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_image:
        # Assure-toi que cette image existe bien dans le dossier images !
        st.image("images/image6.jpg", use_container_width=True)

    st.markdown(
        """
        <div class="disclaimer">
        Le résultat obtenu est une évaluation indicative basée sur un modèle simplifié construit à partir
        du Guide de bonnes pratiques CMRPI/AUSIM. La maturité cyber n'est pas une évaluation du niveau de
        sécurité technique des systèmes d'information d'une entreprise, mais de sa posture générale à
        l'égard des enjeux de cybersécurité.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # fin main-pad

    st.markdown(
        """
        <div class="lower-band">
            <div>
                <h4>Encouragez d'autres PME à agir</h4>
                <p>Aidez d'autres entreprises marocaines à évaluer leur maturité cyber et à accéder
                au Guide CMRPI/AUSIM.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <footer class="custom-footer">
            CMRPI — Espace Maroc Cyberconfiance · Stage PFA 2026 · Projet N°1 — Plateforme d'audit et
            d'évaluation de la maturité cybersécurité des PME marocaines.<br>
            Source : Guide de bonnes pratiques CMRPI/AUSIM — ausimaroc.com/guide-des-bonnes-pratiques-cmrpi
        </footer>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# PAGE — QUESTIONNAIRE
# =====================================================================
def page_questionnaire():
    barre_navigation()

    idx = st.session_state.question_courante
    item = QUESTIONS_FLAT[idx]

    numero_axe = AXES.index(
        next(a for a in AXES if a["nom"] == item["axe"])
    )

    bandeau_hero(fil_ariane_extra=item["axe"])

    st.markdown(
        '<div class="main-pad">',
        unsafe_allow_html=True
    )

    # =========================================================
    # COLONNES : QUESTION + IMAGE
    # =========================================================

    col_question, col_image = st.columns(
        [1.4, 1],
        gap="large"
    )

    # =========================================================
    # CARTE DE LA QUESTION
    # =========================================================

    with col_question:

        with st.container(border=True):

            col_badge, col_progres = st.columns([3, 1])

            with col_badge:
                st.markdown(
                    f'''
                    <div class="axe-badge">
                        AXE {numero_axe} · {item["axe"].upper()}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            with col_progres:
                st.markdown(
                    f'''
                    <div style="text-align:right;">
                        <span class="q-progress-badge">
                            Question {idx + 1}/{TOTAL_QUESTIONS}
                        </span>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            st.markdown(
                f'''
                <div class="q-title">
                    {item["q"]}
                </div>
                ''',
                unsafe_allow_html=True
            )

            reponse_precedente = st.session_state.reponses.get(
                idx,
                None
            )

            choix = st.radio(
                label="reponse",
                options=list(range(len(item["opts"]))),
                format_func=lambda n: item["opts"][n],
                index=reponse_precedente,
                key=f"radio_{idx}",
                label_visibility="collapsed",
            )

        # =====================================================
        # BOUTONS
        # =====================================================

        st.write("")

        col_annuler, col_spacer, col_suivant = st.columns(
            [1, 2, 1]
        )

        with col_annuler:

            if st.button("Annuler"):
                aller_a("accueil")

        with col_suivant:

            label = (
                "Voir le résultat →"
                if idx == TOTAL_QUESTIONS - 1
                else "Suivant →"
            )

            if st.button(label, type="primary"):

                if choix is None:

                    st.error(
                        "Merci de choisir une réponse avant de continuer."
                    )

                else:

                    st.session_state.reponses[idx] = choix

                    if idx == TOTAL_QUESTIONS - 1:

                        enregistrer_resultat()
                        aller_a("resultat")

                    else:

                        st.session_state.question_courante += 1
                        st.rerun()

        # =====================================================
        # BOUTON PRÉCÉDENT
        # =====================================================

        if idx > 0:

            if st.button("← Précédent"):
                st.session_state.question_courante -= 1
                st.rerun()

    # =========================================================
    # IMAGE DE L'AXE
    # =========================================================

    with col_image:

        image_a_afficher = chemin_image_axe(numero_axe)

        # IMPORTANT :
        # On utilise st.image() et non <img src="">
        # car les images sont des fichiers locaux du projet.

        st.image(
            image_a_afficher,
            use_container_width=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
def enregistrer_resultat():
    score = sum(st.session_state.reponses.get(i, 0) for i in INDICES_NOTEES)
    niveau = niveau_maturite(score, SCORE_MAX)
    par_theme = {}
    for axe in AXES:
        if not axe["notee"]:
            continue
        indices = [i for i, q in enumerate(QUESTIONS_FLAT) if q["axe"] == axe["nom"]]
        s = sum(st.session_state.reponses.get(i, 0) for i in indices)
        par_theme[axe["nom"]] = (s, len(indices) * 3)
    st.session_state.historique.append({
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "score": score, "score_max": SCORE_MAX, "niveau": niveau,
        "par_theme": par_theme, "reponses": dict(st.session_state.reponses),
    })


# =====================================================================
# PAGE — RÉSULTAT
# =====================================================================
def page_resultat():
    barre_navigation()
    if not st.session_state.historique:
        aller_a("accueil")
        return
    bandeau_hero(fil_ariane_extra="Résultat")
    dernier = st.session_state.historique[-1]

    st.markdown('<div class="main-pad">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Votre résultat</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Score global</div>'
            f'<div class="metric-value">{dernier["score"]}/{dernier["score_max"]}</div>'
            f'<div class="level-pill">{dernier["niveau"]}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown("**Détail par thème**")
        for nom_axe, (s, m) in dernier["par_theme"].items():
            st.write(f"{nom_axe} — {s}/{m}")
            st.progress(s / m if m else 0)

    st.write("")
    st.markdown("#### Vos priorités")
    faibles = sorted(dernier["reponses"].items(), key=lambda x: x[1])
    top_faibles = [i for i, niveau in faibles if i in INDICES_NOTEES and niveau <= 1][:3]
    if not top_faibles:
        st.success("Bravo, aucune faiblesse majeure détectée sur ce questionnaire !")
    else:
        for rang, i in enumerate(top_faibles, start=1):
            axe_nom = QUESTIONS_FLAT[i]["axe"]
            reco = RECOMMANDATIONS.get(i, "Renforcez cette bonne pratique.")
            st.markdown(f'<div class="reco-box"><div class="reco-theme">{rang}. {axe_nom}</div>{reco}</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("Retour à l'accueil", type="primary"):
        aller_a("accueil")
    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================================
# ROUTAGE
# =====================================================================
PAGES = {"accueil": page_accueil, "questionnaire": page_questionnaire, "resultat": page_resultat}
PAGES[st.session_state.page]()