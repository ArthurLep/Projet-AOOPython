# Projet-AOOPython

# MeetingPro - Gestion de Réservations de Salles

## 👥 Contributeurs
- AIT OUAARAB Yasmine
- LEPROUST Arthur

## 📝 Description du projet

**MeetingPro** est une application de bureau développée en Python avec une interface graphique (Tkinter, CustomTkinter). Elle permet à une entreprise spécialisée dans la location d’espaces de coworking de gérer efficacement les **réservations de salles** par ses clients.  
L’utilisateur peut ajouter des clients et des salles, consulter les disponibilités et effectuer des réservations dans un système simple et intuitif.  
Les données sont stockées de manière persistante via un fichier **JSON**, garantissant la sauvegarde automatique des informations.

## 📁 Structure du projet


### 🖥️ Interface graphique

L’application est destinée à un usage exclusivement administratif. Elle ne propose pas d’interface utilisateur client ni de système d’inscription ou de connexion.

Depuis la page d’accueil, les membres de l’administration peuvent :

- Visualiser la liste des réservations en cours.

- Créer de nouvelles réservations.

- Ajouter, modifier ou supprimer des clients.

- Ajouter, modifier ou supprimer des salles.

Un calendrier interactif (via la bibliothèque tkcalendar) facilite la sélection des dates pour les réservations.

#### 🛠️ Gestion des données

- Les données clients, salles et réservations sont gérées via des classes dédiées organisées en modèle
- La persistance est assurée par des fichiers JSON.

## 📚 Différentes librairies utilisées 
- `CustomTkinter` pour une interface plus moderne et personnalisable. 
- `Tkinter` : bibliothèque graphique standard de Python
- `Pillow` pour la gestion et manipulation d'images  
- `tkcalendar` pour l’intégration du calendrier