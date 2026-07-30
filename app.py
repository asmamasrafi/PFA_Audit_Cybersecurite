import streamlit as st

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

# On structure les données pour les afficher facilement ensuite
questions_data = {
    "Thème 1 : Contexte et exposition aux risques (Non noté)": {
        "description": "Ces questions servent à comprendre l'importance de l'informatique pour votre entreprise.",
        "questions": [
            {"id": "Q1", "titre": "Q1 - Le système informatique est-il indispensable au fonctionnement quotidien de l'entreprise ?", "choix": ["0 : Non, outil facilitant le travail", "1 : Vision transverse", "2 : Outil de transformation", "3 : Oui, outil indispensable"]},
            {"id": "Q2", "titre": "Q2 - Une panne informatique de plusieurs jours aurait-elle un impact important ?", "choix": ["0 : Aucun effet", "1 : Effet faible", "2 : Effet majeur", "3 : Effet bloquant"]},
            {"id": "Q3", "titre": "Q3 - La perte de données aurait-elle des conséquences importantes ?", "choix": ["0 : Aucun effet", "1 : Effet faible", "2 : Effet majeur", "3 : Effet bloquant"]},
            {"id": "Q4", "titre": "Q4 - Une fuite d'informations sensibles nuirait-elle gravement à l'entreprise ?", "choix": ["0 : Aucun effet", "1 : Effet faible", "2 : Effet majeur", "3 : Effet bloquant"]},
            {"id": "Q5", "titre": "Q5 - L'entreprise évolue-t-elle dans un secteur très concurrentiel ?", "choix": ["0 : Pas concurrentiel", "1 : Peu concurrentiel", "2 : Concurrentiel", "3 : Concurrence féroce"]},
            {"id": "Q6", "titre": "Q6 - Le système informatique est-il connecté à internet ou à des partenaires ?", "choix": ["0 : Système isolé", "1 : Connexions limitées", "2 : Fortement interconnecté", "3 : Totalement ouvert"]}
        ]
    },
    "Thème 2 : Gouvernance et organisation": {
        "description": "Ces questions évaluent comment la sécurité est structurée dans votre entreprise.",
        "questions": [
            {"id": "Q7", "titre": "Q7 - Avez-vous mis en place des règles de sécurité informatique ?", "choix": ["0 : Aucune règle définie", "1 : Quelques règles à l'oral", "2 : Règles suivies mais non écrites", "3 : Document écrit et distribué"]},
            {"id": "Q8", "titre": "Q8 - Une personne est-elle chargée de s'occuper de la sécurité ?", "choix": ["0 : Personne", "1 : De temps en temps, non officiel", "2 : Régulièrement, non officiel", "3 : Responsable officiellement désigné"]},
            {"id": "Q9", "titre": "Q9 - Savez-vous exactement quels ordinateurs et logiciels sont utilisés ?", "choix": ["0 : Aucune liste", "1 : Liste incomplète", "2 : Liste mise à jour de temps en temps", "3 : Liste complète et toujours à jour"]},
            {"id": "Q10", "titre": "Q10 - Réfléchissez-vous régulièrement aux risques informatiques ?", "choix": ["0 : Jamais", "1 : De temps en temps, sans méthode", "2 : Régulièrement (une fois par an)", "3 : De façon organisée et structurée"]}
        ]
    },
    "Thème 3 : Accès, mots de passe et réseau": {
        "description": "Sécurisation de vos accès et de vos infrastructures.",
        "questions": [
            {"id": "Q11", "titre": "Q11 - Chaque employé possède-t-il son propre compte ?", "choix": ["0 : Non, comptes partagés", "1 : Une partie seulement", "2 : Tous les employés", "3 : Tous les employés + vérifications"]},
            {"id": "Q12", "titre": "Q12 - Comment sont gérés les mots de passe ?", "choix": ["0 : Aucune règle", "1 : Règles de base, rarement changés", "2 : Corrects et changés parfois", "3 : Complexes et changés régulièrement"]},
            {"id": "Q13", "titre": "Q13 - Quand un employé part, ses accès sont-ils supprimés ?", "choix": ["0 : Jamais", "1 : Avec du retard", "2 : La plupart du temps", "3 : Systématiquement le jour même"]},
            {"id": "Q14", "titre": "Q14 - Le réseau Wi-Fi est-il protégé ?", "choix": ["0 : Pas de mot de passe", "1 : Même mot de passe pour tous", "2 : Mot de passe partagé", "3 : Réseaux séparés (visiteurs/employés)"]},
            {"id": "Q15", "titre": "Q15 - Les ordinateurs sont-ils protégés par un antivirus ?", "choix": ["0 : Aucun antivirus", "1 : Sur certains ordinateurs", "2 : Partout mais pas à jour", "3 : Installé et mis à jour partout"]}
        ]
    },
    "Thème 4 : Sensibilisation et sécurité humaine": {
        "description": "Formation et sensibilisation de vos collaborateurs.",
        "questions": [
            {"id": "Q16", "titre": "Q16 - Vos employés sont-ils informés des risques (virus, arnaques) ?", "choix": ["0 : Aucune information", "1 : Conseils informels", "2 : Information occasionnelle", "3 : Formation annuelle organisée"]},
            {"id": "Q17", "titre": "Q17 - Vos employés savent-ils reconnaître un email suspect (phishing) ?", "choix": ["0 : Non", "1 : Quelques employés", "2 : La plupart", "3 : Tous les employés"]},
            {"id": "Q18", "titre": "Q18 - L'accès aux locaux (serveurs) est-il protégé ?", "choix": ["0 : Aucune protection", "1 : Précautions de bon sens", "2 : Accès limité", "3 : Accès strictement contrôlé (badge/clé)"]},
            {"id": "Q19", "titre": "Q19 - Les informations confidentielles sont-elles protégées ?", "choix": ["0 : Aucune protection", "1 : Limité informellement", "2 : Restreint non officiellement", "3 : Restreint et protégé (mot de passe)"]}
        ]
    },
    "Thème 5 : Sauvegarde, incidents et conformité": {
        "description": "Préparation aux crises et respect de la législation.",
        "questions": [
            {"id": "Q20", "titre": "Q20 - Les données importantes sont-elles sauvegardées ?", "choix": ["0 : Aucune sauvegarde", "1 : De temps en temps", "2 : Régulièrement sans vérification", "3 : Régulièrement avec vérification"]},
            {"id": "Q21", "titre": "Q21 - Où sont conservées les sauvegardes ?", "choix": ["0 : Au même endroit (même PC)", "1 : Copie ailleurs de temps en temps", "2 : Copie ailleurs régulièrement", "3 : Toujours ailleurs (Cloud/Disque dur)"]},
            {"id": "Q22", "titre": "Q22 - En cas de problème informatique, vos employés savent-ils quoi faire ?", "choix": ["0 : Aucune consigne", "1 : Au cas par cas", "2 : Consignes pour quelques personnes", "3 : Procédure écrite connue de tous"]},
            {"id": "Q23", "titre": "Q23 - En cas de panne majeure, pourriez-vous continuer à fonctionner ?", "choix": ["0 : Aucun plan", "1 : Secours ponctuels", "2 : Plan non testé", "3 : Plan complet et testé"]},
            {"id": "Q24", "titre": "Q24 - Respectez-vous la loi 09-08 sur les données personnelles ?", "choix": ["0 : Non respectée", "1 : Isolément", "2 : Généralement respectée", "3 : Vérification régulière de la conformité"]}
        ]
    }
}

themes_list = list(questions_data.keys())
noms_etapes = ["Accueil"] + [f"Thème {i+1}" for i in range(len(themes_list))] + ["Résultats"]

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
        # st.radio permet d'afficher les choix multiples
        st.session_state.reponses[q["id"]] = st.radio(
            q["titre"],
            options=q["choix"],
            # On pré-sélectionne la réponse si elle existe déjà dans la mémoire
            index=int(st.session_state.reponses.get(q["id"])[0]) if q["id"] in st.session_state.reponses else 0
        )
        st.write("") # Espace visuel
    
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
    
    # CALCUL DU SCORE (Uniquement les questions Q7 à Q24)
    score_total = 0
    for i in range(7, 25):
        id_question = f"Q{i}"
        # La réponse stockée ressemble à "2 : blabla". On récupère juste le premier caractère "2" qu'on convertit en entier.
        reponse_str = st.session_state.reponses.get(id_question, "0")
        points = int(reponse_str[0]) 
        score_total += points

    # Affichage du score
    st.markdown(f"### Votre score de maturité : **{score_total} / 54**")
    st.progress(score_total / 54) # Barre de progression visuelle
    
    # LOGIQUE D'INTERPRETATION DU SCORE
    if score_total <= 14:
        st.error("🚨 **Niveau 1 (Initial)** : Bonnes pratiques largement absentes, forte exposition aux risques. Une action urgente est recommandée.")
    elif score_total <= 27:
        st.warning("⚠️ **Niveau 2 (Basique)** : Quelques bonnes pratiques isolées, mais pas de démarche structurée.")
    elif score_total <= 41:
        st.info("💡 **Niveau 3 (Intermédiaire)** : Pratiques structurées sur la majorité des thèmes. Continuez ainsi !")
    else:
        st.success("🏆 **Niveau 4 (Avancé)** : Bonnes pratiques largement intégrées dans le fonctionnement quotidien. Excellent !")
        
    st.markdown("---")
    st.button("🔄 Recommencer l'audit", on_click=recommencer)