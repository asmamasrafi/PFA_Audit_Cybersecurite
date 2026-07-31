#  CyberAudit PME

**CyberAudit PME** est une application web interactive développée avec **Streamlit**, conçue pour permettre aux petites et moyennes entreprises marocaines d'évaluer leur niveau de maturité en matière de cybersécurité.

## Description du projet
Basée sur le **Guide des bonnes pratiques CMRPI/AUSIM**, cette plateforme propose un questionnaire structuré en 5 thèmes clés pour auditer la sécurité organisationnelle et technique des structures[cite: 1] :
1. **Contexte et exposition aux risques** (Questions non notées pour la qualification du système d'information)[cite: 1].
2. **Gouvernance et organisation**[cite: 1].
3. **Accès, mots de passe et réseau**[cite: 1].
4. **Sensibilisation et sécurité humaine**[cite: 1].
5. **Sauvegarde, incidents et conformité** (incluant la conformité à la loi marocaine 09-08 sur la protection des données personnelles)[cite: 1].

## Fonctionnalités principales
* **Navigation étape par étape :** Interface fluide gérant dynamiquement l'état des réponses et la progression de l'utilisateur.
* **Moteur de scoring automatisé :** Calcul instantané du score de maturité sur un total de **54 points** (répartis sur les 18 questions évaluées de 0 à 3)[cite: 1].
* **Restitution des résultats :** Affichage visuel du score avec une interprétation claire selon 4 niveaux de maturité (Initial, Basique, Intermédiaire, Avancé)[cite: 1].

## Stack technique
* **Langage :** Python
* **Framework Interface :** Streamlit
