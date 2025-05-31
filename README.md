# Projet AOOPython

# MeetingPro – Gestion des Réservations de Salles

## 👥 Contributeurs

- AIT OUAARAB Yasmine
- LEPROUST Arthur

## 📝 Description du projet

**MeetingPro** est une application de bureau développée en Python, avec une interface graphique conçue grâce à Tkinter et CustomTkinter. Elle permet à une entreprise spécialisée dans la location d’espaces de coworking de gérer efficacement les **réservations de salles** par ses clients.

L’utilisateur peut ajouter des clients et des salles, consulter les disponibilités, puis effectuer des réservations via une interface simple et intuitive. Les données sont stockées de manière persistante dans des fichiers **JSON**, garantissant la sauvegarde automatique des informations.

## 📁 Structure du projet

### 🖥️ Interface graphique

L’application est destinée à un usage exclusivement administratif. Elle ne propose pas d’interface client ni de système d’inscription ou de connexion.

Depuis la page d’accueil, les membres de l’administration peuvent :

- Visualiser la liste des réservations en cours.
- Créer de nouvelles réservations.
- Ajouter, modifier ou supprimer des clients.
- Ajouter, modifier ou supprimer des salles.

Un calendrier interactif, intégré via la bibliothèque `tkcalendar`, facilite la sélection des dates pour les réservations.

#### 🛠️ Gestion des données

- Les données clients, salles et réservations sont modélisées via des classes dédiées.
- La persistance est assurée par des fichiers au format JSON.

## 📚 Librairies utilisées

- `CustomTkinter` : pour une interface moderne et personnalisable.
- `Tkinter` : bibliothèque graphique standard de Python.
- `tkcalendar` : pour l’intégration du calendrier.

## 🚀 Lancement de l’application

L’interface graphique se lance directement via le fichier `main.py`.
