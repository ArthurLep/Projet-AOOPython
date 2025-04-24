# Projet-AOOPython

# MeetingPro - Gestion de Réservations de Salles

## 👥 Contributeurs
- AIT OUAARAB Yasmine
- LEPROUST Arthur

## 📝 Description du projet

**MeetingPro** est une application de bureau développée en Python avec une interface graphique (Tkinter). Elle permet à une entreprise spécialisée dans la location d’espaces de coworking de gérer efficacement les **réservations de salles** par ses clients.  
L’utilisateur peut ajouter des clients et des salles, consulter les disponibilités et effectuer des réservations dans un système simple et intuitif.  
Les données sont stockées de manière persistante via un fichier **JSON**, garantissant la sauvegarde automatique des informations.

## 📁 Structure du projet


### 🖥️ Interface graphique

L'application démarre avec une **interface de connexion/inscription**, permettant d’accueillir deux types d’utilisateurs :

- **Client** : doit fournir une adresse e-mail et un mot de passe pour accéder à la plateforme de réservation.
- **Administrateur** : accède à des fonctionnalités de gestion via une interface sécurisée.

L’interface permet aussi de s’enregistrer en tant que **nouvel utilisateur** via une section "signup", en saisissant les informations nécessaires (nom, email, mot de passe…).

Chaque utilisateur est ensuite redirigé vers une interface spécifique selon son rôle.

#### 🧑‍💻 Interface Utilisateur

L'interface client comprend plusieurs fonctionnalités clés :
- **Visualisation des réservations** en cours.
- **Création de nouvelles réservations** de salles disponibles.
- **Annulation de réservations** existantes.
- **Affichage d'un calendrier interactif** (via `tkcalendar`) dès la page d'accueil, permettant une navigation dans les dates de réservation.

## 📚 Différentes librairies utilisées 
- `CustomTkinter` pour une interface plus moderne et réactive. 
- `Pillow` pour la gestion des images  
- `tkcalendar` pour l’intégration du calendrier