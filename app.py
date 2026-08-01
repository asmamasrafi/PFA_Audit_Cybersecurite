import io
import streamlit as st

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

# Configuration de base de la page web
st.set_page_config(
    page_title="CyberAudit PME",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Streamlit recharge la page à chaque clic. On utilise session_state pour mémoriser l'étape actuelle et les réponses.
if 'etape' not in st.session_state:
    st.session_state.etape = 0
if 'reponses' not in st.session_state:
    st.session_state.reponses = {}

# Fonction pour passer à l'étape suivante
def page_suivante():
    st.session_state.etape += 1

# Fonction pour revenir à l'étape précédente
def page_precedente():
    st.session_state.etape -= 1

# Fonction pour recommencer l'audit
def recommencer():
    st.session_state.etape = 0
    st.session_state.reponses = {}

# Structure des données mise à jour selon le guide CMRPI/AUSIM
questions_data = {
    "Thème 1 : Contexte et exposition aux risques": {
        "description": "Ces questions servent à comprendre l'importance de l'informatique pour l'entreprise, afin de mieux interpréter le score obtenu. Elles ne comptent pas dans le calcul du score.",
        "questions": [
            {"id": "Q1", "titre": "Q1 - Le système informatique est-il indispensable au fonctionnement quotidien de l'entreprise ?", "choix": ["Non", "Oui"]},
            {"id": "Q2", "titre": "Q2 - Une panne informatique de plusieurs jours aurait-elle un impact important sur l'activité ?", "choix": ["Non", "Oui"]},
            {"id": "Q3", "titre": "Q3 - La perte ou la modification accidentelle de données aurait-elle des conséquences importantes ?", "choix": ["Non", "Oui"]},
            {"id": "Q4", "titre": "Q4 - Une fuite d'informations sensibles (clients, finances) nuirait-elle gravement à l'entreprise ?", "choix": ["Non", "Oui"]},
            {"id": "Q5", "titre": "Q5 - L'entreprise évolue-t-elle dans un secteur très concurrentiel où l'information a de la valeur ?", "choix": ["Non", "Oui"]},
            {"id": "Q6", "titre": "Q6 - Le système informatique est-il connecté à internet ou à des partenaires externes ?", "choix": ["Non", "Oui"]}
        ]
    },
    "Thème 2 : Gouvernance et organisation": {
        "description": "Ces questions évaluent comment la sécurité est structurée dans votre entreprise.",
        "questions": [
            {"id": "Q7", "titre": "Q7 - Avez-vous mis en place des règles de sécurité informatique dans votre entreprise ?", "choix": [
                "0 : Aucune règle définie chacun fait comme il veut.",
                "1 : Quelques règles existent, mais elles sont seulement dites à l'oral et pas toujours suivies.",
                "2 : Des règles sont suivies au quotidien par les employés, mais elles ne sont écrites nulle part.",
                "3 : Il existe un document écrit avec les règles de sécurité, distribué à tous les employés."
            ]},
            {"id": "Q8", "titre": "Q8 - Une personne est-elle chargée de s'occuper de la sécurité informatique de l'entreprise ?", "choix": [
                "0 : Personne ne s'occupe de la sécurité informatique.",
                "1 : Quelqu'un s'en occupe de temps en temps, sans que ce soit son rôle officiel.",
                "2 : Une personne s'en occupe régulièrement, mais ce n'est pas écrit dans ses fonctions.",
                "3 : Une personne est officiellement désignée responsable, et tout le monde le sait."
            ]},
            {"id": "Q9", "titre": "Q9 - Savez-vous exactement quels ordinateurs et logiciels sont utilisés dans votre entreprise ?", "choix": [
                "0 : Aucune liste n'existe personne ne sait précisément ce qui est utilisé.",
                "1 : Une liste existe mais elle est incomplète et rarement mise à jour.",
                "2 : Une liste existe et elle est mise à jour de temps en temps, mais pas systématiquement.",
                "3 : Une liste complète existe et elle est tenue à jour à chaque changement."
            ]},
            {"id": "Q10", "titre": "Q10 - Réfléchissez-vous régulièrement aux risques informatiques qui menacent votre entreprise (virus, panne, vol de matériel) ?", "choix": [
                "0 : Jamais ces risques ne sont pas évalués.",
                "1 : De temps en temps, mais sans méthode particulière ni suivi.",
                "2 : Régulièrement, en général une fois dans l'année.",
                "3 : Au moins une fois par an, de façon organisée et structurée."
            ]}
        ]
    },
    "Thème 3 : Accès, mots de passe et réseau": {
        "description": "Sécurisation de vos accès et de vos infrastructures.",
        "questions": [
            {"id": "Q11", "titre": "Q11 - Chaque employé possède-t-il son propre compte pour se connecter aux ordinateurs et aux logiciels ?", "choix": [
                "0 : Non plusieurs employés utilisent le même identifiant et le même mot de passe.",
                "1 : Une partie seulement des employés a un compte individuel.",
                "2 : Tous les employés ont un compte individuel.",
                "3 : Tous les employés ont un compte individuel, et l'entreprise vérifie qui accède à quoi."
            ]},
            {"id": "Q12", "titre": "Q12 - Comment sont gérés les mots de passe dans votre entreprise ?", "choix": [
                "0 : Il n'y a aucune règle particulière sur les mots de passe.",
                "1 : Il existe des règles de base, mais les mots de passe sont rarement changés.",
                "2 : Les mots de passe sont corrects, et changés de temps en temps.",
                "3 : Les mots de passe sont complexes (lettres, chiffres, symboles) et changés régulièrement."
            ]},
            {"id": "Q13", "titre": "Q13 - Quand un employé quitte l'entreprise, ses accès informatiques sont-ils supprimés ?", "choix": [
                "0 : Non, jamais fait d'anciens employés peuvent encore avoir accès.",
                "1 : Cela arrive, mais souvent avec du retard.",
                "2 : Cela est fait la plupart du temps.",
                "3 : Cela est fait systématiquement, dès le jour du départ de l'employé."
            ]},
            {"id": "Q14", "titre": "Q14 - Le réseau Wi-Fi de votre entreprise est-il protégé ?", "choix": [
                "0 : Non, il n'y a pas de mot de passe sur le Wi-Fi.",
                "1 : Il y a un mot de passe, mais il est le même pour les employés et pour les visiteurs.",
                "2 : Il y a un mot de passe, mais il est connu et partagé largement.",
                "3 : Il existe un réseau séparé pour les visiteurs et un réseau protégé pour les employés."
            ]},
            {"id": "Q15", "titre": "Q15 - Les ordinateurs de votre entreprise sont-ils protégés par un antivirus ?", "choix": [
                "0 : Non, aucun antivirus n'est installé.",
                "1 : Un antivirus est installé sur certains ordinateurs seulement.",
                "2 : Un antivirus est installé partout, mais il n'est pas toujours mis à jour.",
                "3 : Un antivirus est installé et mis à jour sur tous les ordinateurs."
            ]}
        ]
    },
    "Thème 4 : Sensibilisation et sécurité humaine": {
        "description": "Formation et sensibilisation de vos collaborateurs.",
        "questions": [
            {"id": "Q16", "titre": "Q16 - Vos employés sont-ils informés des risques liés à internet et aux emails (virus, arnaques) ?", "choix": [
                "0 : Non, aucune information n'est donnée à ce sujet.",
                "1 : Quelques conseils sont donnés de temps en temps, de manière informelle.",
                "2 : Une information est donnée de temps en temps, mais sans régularité.",
                "3 : Une formation ou une information est organisée au moins une fois par an."
            ]},
            {"id": "Q17", "titre": "Q17 - Vos employés savent-ils reconnaître un email suspect ou une tentative d'arnaque (phishing) ?", "choix": [
                "0 : Non, les employés ne sont pas informés sur ce sujet.",
                "1 : Quelques employés seulement savent reconnaître un email suspect.",
                "2 : La plupart des employés savent le reconnaître.",
                "3 : Tous les employés savent reconnaître un email suspect et savent quoi faire."
            ]},
            {"id": "Q18", "titre": "Q18 - L'accès aux locaux où se trouvent les ordinateurs et serveurs importants est-il protégé ?", "choix": [
                "0 : Non, aucune protection particulière (portes ouvertes, accès libre).",
                "1 : Quelques précautions de bon sens sont prises, mais rien d'organisé.",
                "2 : L'accès à certaines zones sensibles est limité.",
                "3 : L'accès est strictement contrôlé, par exemple avec une porte fermée à clé ou un badge."
            ]},
            {"id": "Q19", "titre": "Q19 - Les informations confidentielles (données des clients, dossiers du personnel) sont-elles protégées ?", "choix": [
                "0 : Non, aucune protection particulière n'est mise en place.",
                "1 : L'accès est limité, mais de façon informelle, sans règle précise.",
                "2 : L'accès est restreint, mais ce n'est pas écrit officiellement.",
                "3 : L'accès est restreint et protégé, par exemple par un mot de passe ou un dossier réservé."
            ]}
        ]
    },
    "Thème 5 : Sauvegarde, incidents et conformité": {
        "description": "Préparation aux crises et respect de la législation.",
        "questions": [
            {"id": "Q20", "titre": "Q20 - Les données importantes de votre entreprise (factures, clients, documents) sont-elles sauvegardées ?", "choix": [
                "0 : Non, il n'y a aucune sauvegarde.",
                "1 : Une sauvegarde est faite de temps en temps, sans planification.",
                "2 : Une sauvegarde est faite régulièrement, mais elle n'est jamais vérifiée.",
                "3 : Une sauvegarde est faite régulièrement et son bon fonctionnement est vérifié."
            ]},
            {"id": "Q21", "titre": "Q21 - Où sont conservées les sauvegardes de vos données ?", "choix": [
                "0 : Toujours au même endroit que les données d'origine (même ordinateur ou serveur).",
                "1 : Une copie est faite ailleurs, mais seulement de temps en temps.",
                "2 : Une copie est faite ailleurs régulièrement.",
                "3 : Les sauvegardes sont toujours conservées ailleurs (disque externe ou cloud)."
            ]},
            {"id": "Q22", "titre": "Q22 - En cas de problème informatique (panne, piratage), vos employés savent-ils quoi faire ?", "choix": [
                "0 : Non, il n'existe aucune consigne à ce sujet.",
                "1 : On réagit au cas par cas, sans règle précise.",
                "2 : Certaines consignes existent et sont connues de quelques personnes seulement.",
                "3 : Il existe une procédure écrite, connue de tous les employés."
            ]},
            {"id": "Q23", "titre": "Q23 - Si votre système informatique tombait en panne pendant plusieurs jours, votre entreprise pourrait-elle continuer à fonctionner ?", "choix": [
                "0 : Non, aucun plan n'est prévu pour ce genre de situation.",
                "1 : Quelques solutions de secours existent, mais de façon ponctuelle.",
                "2 : Un plan existe, mais il n'est pas complet ni testé.",
                "3 : Un plan complet existe et a déjà été testé pour vérifier qu'il fonctionne."
            ]},
            {"id": "Q24", "titre": "Q24 - Votre entreprise respecte-t-elle les règles marocaines sur la protection des données personnelles (loi 09-08) ?", "choix": [
                "0 : Non, ces règles ne sont pas respectées.",
                "1 : Elles sont respectées de façon isolée, sans démarche organisée.",
                "2 : Elles sont généralement respectées.",
                "3 : Elles sont respectées et l'entreprise vérifie régulièrement qu'elle est en conformité."
            ]}
        ]
    }
}

themes_list = list(questions_data.keys())
noms_etapes = ["Accueil"] + [f"Thème {i+1}" for i in range(len(themes_list))] + ["Résultats"]

# ------------------------------------------------------------------
# NIVEAUX DE MATURITE ET RECOMMANDATIONS
# Chaque niveau est défini par un seuil de score (sur 54) et associé
# à 2-3 recommandations prioritaires à donner à la PME.
# ------------------------------------------------------------------
NIVEAUX = [
    {
        "seuil_max": 14,
        "nom": "Niveau 1 (Initial)",
        "emoji": "🚨",
        "description": "Bonnes pratiques largement absentes, forte exposition aux risques. Une action urgente est recommandée.",
        "recommandations": [
            "Mettre en place immédiatement des sauvegardes régulières des données, stockées sur un support différent (disque externe ou cloud).",
            "Installer un antivirus à jour sur tous les postes et créer un compte informatique individuel pour chaque employé.",
            "Rédiger une liste minimale de règles de sécurité (mots de passe, usage d'internet) et la communiquer à tous."
        ]
    },
    {
        "seuil_max": 27,
        "nom": "Niveau 2 (Basique)",
        "emoji": "⚠️",
        "description": "Quelques bonnes pratiques isolées, mais pas de démarche structurée.",
        "recommandations": [
            "Désigner officiellement une personne responsable de la sécurité informatique, même à temps partiel.",
            "Formaliser par écrit les règles de sécurité existantes et organiser une sensibilisation annuelle au phishing.",
            "Vérifier régulièrement que les sauvegardes fonctionnent réellement (test de restauration)."
        ]
    },
    {
        "seuil_max": 41,
        "nom": "Niveau 3 (Intermédiaire)",
        "emoji": "💡",
        "description": "Pratiques structurées sur la majorité des thèmes. Continuez ainsi !",
        "recommandations": [
            "Formaliser une procédure écrite de gestion des incidents, connue de tous les employés.",
            "Élaborer et tester un plan de continuité d'activité en cas de panne prolongée.",
            "Vérifier annuellement la conformité à la loi 09-08 sur la protection des données personnelles."
        ]
    },
    {
        "seuil_max": 54,
        "nom": "Niveau 4 (Avancé)",
        "emoji": "🏆",
        "description": "Bonnes pratiques largement intégrées dans le fonctionnement quotidien. Excellent !",
        "recommandations": [
            "Maintenir une veille sur les nouvelles menaces et mettre à jour régulièrement les procédures existantes.",
            "Réaliser des audits de sécurité périodiques, idéalement avec un regard externe.",
            "Continuer à sensibiliser les nouveaux employés dès leur arrivée (onboarding sécurité)."
        ]
    },
]


def obtenir_niveau(score_total: int) -> dict:
    """Retourne le dictionnaire du niveau de maturité correspondant au score."""
    for niveau in NIVEAUX:
        if score_total <= niveau["seuil_max"]:
            return niveau
    return NIVEAUX[-1]


def generer_pdf_rapport(score_total: int, niveau: dict, nom_entreprise: str = "") -> bytes:
    """
    Génère un rapport PDF (en mémoire) contenant le score de maturité
    cybersécurité et 2-3 recommandations selon le niveau atteint.
    Retourne le contenu du PDF sous forme de bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle(
        "TitrePrincipal", parent=styles["Title"], fontSize=20,
        textColor=colors.HexColor("#1F2937"), spaceAfter=6
    )
    style_sous_titre = ParagraphStyle(
        "SousTitre", parent=styles["Normal"], fontSize=11,
        textColor=colors.HexColor("#6B7280"), spaceAfter=20
    )
    style_h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontSize=14,
        textColor=colors.HexColor("#1F2937"), spaceBefore=16, spaceAfter=8
    )
    style_corps = ParagraphStyle(
        "Corps", parent=styles["Normal"], fontSize=11, leading=16
    )
    style_reco = ParagraphStyle(
        "Reco", parent=styles["Normal"], fontSize=11, leading=16,
        leftIndent=10, spaceAfter=8
    )

    elements = []

    # En-tête
    elements.append(Paragraph("🛡️ Rapport d'audit CyberAudit PME", style_titre))
    sous_titre = "Évaluation de la maturité cybersécurité (référentiel CMRPI/AUSIM)"
    if nom_entreprise:
        sous_titre = f"{nom_entreprise} — {sous_titre}"
    elements.append(Paragraph(sous_titre, style_sous_titre))

    # Score
    elements.append(Paragraph("Score de maturité", style_h2))
    couleur_niveau = {
        "Niveau 1 (Initial)": colors.HexColor("#DC2626"),
        "Niveau 2 (Basique)": colors.HexColor("#D97706"),
        "Niveau 3 (Intermédiaire)": colors.HexColor("#2563EB"),
        "Niveau 4 (Avancé)": colors.HexColor("#16A34A"),
    }.get(niveau["nom"], colors.black)

    table_score = Table(
        [[f"{score_total} / 54", f"{niveau['emoji']} {niveau['nom']}"]],
        colWidths=[6 * cm, 9 * cm]
    )
    table_score.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (0, 0), 22),
        ("FONTSIZE", (1, 0), (1, 0), 14),
        ("TEXTCOLOR", (0, 0), (0, 0), couleur_niveau),
        ("TEXTCOLOR", (1, 0), (1, 0), couleur_niveau),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(table_score)
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(niveau["description"], style_corps))

    # Recommandations
    elements.append(Paragraph("Recommandations prioritaires", style_h2))
    for i, reco in enumerate(niveau["recommandations"], start=1):
        elements.append(Paragraph(f"<b>{i}.</b> {reco}", style_reco))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        "<i>Ce rapport est généré automatiquement à partir de vos réponses et fournit "
        "des pistes générales. Il ne remplace pas un audit de sécurité approfondi réalisé "
        "par un professionnel.</i>",
        ParagraphStyle("Note", parent=styles["Normal"], fontSize=9, textColor=colors.grey)
    ))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


with st.sidebar:
    st.title("🛡️ CyberAudit PME")
    st.markdown("---")
    st.write("**Progression :**")
    for i, nom in enumerate(noms_etapes):
        if i == st.session_state.etape:
            st.markdown(f"👉 **{nom}**")
        elif i < st.session_state.etape:
            st.markdown(f"✅ *{nom}*")
        else:
            st.markdown(f"⏳ {nom}")

# ETAPE 0 : Page d'accueil
if st.session_state.etape == 0:
    st.title("Bienvenue sur la plateforme d'audit cybersécurité")
    st.write("Cet outil vous permet d'évaluer la maturité de votre PME face aux risques cybernétiques, selon le référentiel CMRPI/AUSIM.")
    st.info("Le questionnaire est divisé en 5 thèmes. Cela vous prendra environ 5 à 10 minutes.")
    st.button("Commencer l'audit 🚀", on_click=page_suivante)

# ETAPES 1 à 5 : Affichage des thèmes de questions
elif 1 <= st.session_state.etape <= 5:
    theme_actuel = themes_list[st.session_state.etape - 1]
    donnees_theme = questions_data[theme_actuel]

    st.header(theme_actuel)
    st.write(f"*{donnees_theme['description']}*")
    st.markdown("---")

    # Affichage des questions du thème
    for q in donnees_theme["questions"]:
        valeur_actuelle = st.session_state.reponses.get(q["id"])
        if st.session_state.etape == 1:
            index_defaut = q["choix"].index(valeur_actuelle) if valeur_actuelle in q["choix"] else 0
        else:
            index_defaut = int(valeur_actuelle[0]) if valeur_actuelle and valeur_actuelle[0].isdigit() else 0

        st.session_state.reponses[q["id"]] = st.radio(
            q["titre"],
            options=q["choix"],
            index=index_defaut
        )
        st.write("")  # Espace visuel

    # Boutons de navigation
    col1, col2 = st.columns(2)
    with col1:
        st.button("⬅️ Précédent", on_click=page_precedente)
    with col2:
        if st.session_state.etape < 5:
            st.button("Suivant ➡️", on_click=page_suivante)
        else:
            st.button("Terminer et voir le score 🏁", on_click=page_suivante, type="primary")

elif st.session_state.etape == 6:
    st.title("📊 Résultats de votre Audit")

    # CALCUL DU SCORE (Uniquement les questions Q7 à Q24 - Thèmes 2 à 5)
    score_total = 0
    for i in range(7, 25):
        id_question = f"Q{i}"
        reponse_str = st.session_state.reponses.get(id_question, "0")
        points = int(reponse_str[0])
        score_total += points

    # Détermination du niveau (utilisé pour l'affichage ET pour le PDF)
    niveau = obtenir_niveau(score_total)

    # Affichage du score
    st.markdown(f"### Votre score de maturité : **{score_total} / 54**")
    st.progress(score_total / 54)  # Barre de progression visuelle

    # Affichage du niveau (mêmes seuils qu'avant, factorisés dans NIVEAUX)
    boite = {14: st.error, 27: st.warning, 41: st.info, 54: st.success}[niveau["seuil_max"]]
    boite(f"{niveau['emoji']} **{niveau['nom']}** : {niveau['description']}")

    st.markdown("#### 📝 Recommandations prioritaires")
    for i, reco in enumerate(niveau["recommandations"], start=1):
        st.markdown(f"{i}. {reco}")

    st.markdown("---")

    # --- Génération et téléchargement du rapport PDF ---
    nom_entreprise = st.text_input("Nom de l'entreprise (optionnel, apparaîtra sur le rapport)", value="")
    pdf_bytes = generer_pdf_rapport(score_total, niveau, nom_entreprise)
    st.download_button(
        label="📄 Télécharger le rapport PDF",
        data=pdf_bytes,
        file_name="rapport_cyberaudit_pme.pdf",
        mime="application/pdf"
    )

    st.button("🔄 Recommencer l'audit", on_click=recommencer)