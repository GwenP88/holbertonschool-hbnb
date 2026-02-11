# 📘 Explanatory Notes – Detailed Class Diagram - English version

## 1. Overview

The Business Logic Layer represents the core domain of the HBnB application.  
It defines the main entities of the system, their attributes, behaviors, and relationships.

The primary entities modeled in this layer are:

- **User**
- **Place**
- **Review**
- **Amenity**

All entities inherit from an abstract `BaseModel` class, ensuring consistency and shared core attributes across the system.

---

## 2. BaseModel (Abstract Class)

`BaseModel` is an abstract superclass that provides common attributes and behaviors shared by all domain entities.

### Key Attributes

- `id: UUID4` – Unique identifier for each entity instance  
- `created_at: DateTime` – Timestamp of object creation  
- `updated_at: DateTime` – Timestamp of last update  

### Key Methods

- `save()` – Persists changes  
- `update_time()` – Updates the modification timestamp  

This abstraction ensures standardization and avoids duplication of shared properties across domain classes.

---

## 3. User Entity

The `User` class represents individuals interacting with the platform.

### Key Attributes

- `first_name`
- `last_name`
- `email`
- `password`
- `is_admin`

### Key Responsibilities

- Managing user profile data  
- Creating and updating user information  
- Determining ownership of places  
- Managing authentication-related behavior  

### Relationships

- A **User can own multiple Places** (`1 → 0..*`)  
- A **User can write multiple Reviews** (`1 → 0..*`)  
- Each Review has exactly **one author**

---

## 4. Place Entity

The `Place` class represents properties listed on the platform.

### Key Attributes

- `title`
- `description`
- `price`
- `latitude`
- `longitude`
- `owner: User`

### Key Responsibilities

- Managing listing information  
- Associating amenities  
- Managing related reviews  

### Relationships

- A **Place belongs to exactly one User (owner)**  
- A **Place can have multiple Reviews** (`1 → 0..*`)  
- A **Place can have multiple Amenities**, and an Amenity can belong to multiple Places (many-to-many relationship)  

The relationship between `Place` and `Review` is modeled as a **composition**, meaning a Review cannot exist without its associated Place.

---

## 5. Review Entity

The `Review` class represents feedback left by users on places.

### Key Attributes

- `rating`
- `comment`
- `author: User`
- `place: Place`

### Key Responsibilities

- Storing user feedback  
- Ensuring rating integrity  
- Linking authors to places  

### Relationships

- A **Review is written by exactly one User**  
- A **Review belongs to exactly one Place**  

This ensures traceability and accountability within the platform.

---

## 6. Amenity Entity

The `Amenity` class represents features available in a place (e.g., WiFi, TV, Air conditioning).

### Key Attributes

- `name`
- `description`

### Key Responsibilities

- Defining available features  
- Being associated with multiple Places  

### Relationships

- An **Amenity can be associated with multiple Places**  
- A **Place can include multiple Amenities**

This many-to-many association increases flexibility and avoids duplication of amenity definitions.

---

## 7. Relationship Design Rationale

The class relationships reflect real-world business logic:

- Users own Places.  
- Users write Reviews.  
- Reviews are tightly coupled to Places.  
- Amenities are shared reusable resources.  

The use of inheritance via `BaseModel` ensures structural consistency, while associations and compositions clearly represent domain dependencies.

This design promotes:

- High cohesion within entities  
- Clear responsibility separation  
- Maintainability and scalability  
- Strong domain modeling  

---

## 8. Visibility Modifiers in the Diagram

The class diagram uses UML visibility symbols:

- `+` **Public**: Accessible from other classes  
- `-` **Private**: Accessible only within the class  
- `#` **Protected**: Accessible within the class and its subclasses  

In this model:

- Core attributes are marked as **private (-)** to enforce encapsulation.  
- Shared attributes in `BaseModel` are **protected (#)** to allow inheritance.  
- Methods are generally **public (+)** to define the class interface.  

Encapsulation ensures that internal data cannot be modified directly and must go through controlled methods.

---

# 📘 Notes explicatives – Diagramme de classes - version Française

## 1. Vue d’ensemble

La Business Logic Layer représente le cœur métier de l’application HBnB.  
Elle définit les entités principales du système, leurs attributs, leurs comportements et leurs relations.

Les entités principales sont :

- **User**
- **Place**
- **Review**
- **Amenity**

Toutes les entités héritent d’une classe abstraite `BaseModel`, garantissant la cohérence des attributs communs.

---

## 2. BaseModel (Classe abstraite)

`BaseModel` fournit les attributs et comportements communs à toutes les entités métier.

### Attributs principaux

- `id: UUID4` – Identifiant unique  
- `created_at: DateTime` – Date de création  
- `updated_at: DateTime` – Date de dernière modification  

### Méthodes principales

- `save()` – Sauvegarde l’objet  
- `update_time()` – Met à jour le timestamp  

Cette abstraction évite la duplication de code et garantit une structure homogène.

---

## 3. Entité User

La classe `User` représente un utilisateur de la plateforme.

### Attributs principaux

- `first_name`
- `last_name`
- `email`
- `password`
- `is_admin`

### Responsabilités

- Gérer les informations de profil  
- Créer et modifier des données utilisateur  
- Déterminer la propriété d’un logement  
- Gérer certains comportements liés à l’authentification  

### Relations

- Un **User peut posséder plusieurs Places**  
- Un **User peut écrire plusieurs Reviews**  
- Chaque Review possède un seul auteur  

---

## 4. Entité Place

La classe `Place` représente un logement proposé sur la plateforme.

### Attributs principaux

- `title`
- `description`
- `price`
- `latitude`
- `longitude`
- `owner: User`

### Responsabilités

- Gérer les informations du logement  
- Associer des équipements  
- Gérer les avis associés  

### Relations

- Une **Place appartient à un seul User**  
- Une **Place peut avoir plusieurs Reviews**  
- Une **Place peut avoir plusieurs Amenities**, et une Amenity peut être liée à plusieurs Places  

La relation `Place–Review` est modélisée comme une **composition**, ce qui signifie qu’un Review ne peut exister sans sa Place associée.

---

## 5. Entité Review

La classe `Review` représente un avis laissé par un utilisateur.

### Attributs principaux

- `rating`
- `comment`
- `author: User`
- `place: Place`

### Responsabilités

- Stocker les avis  
- Garantir l’intégrité des évaluations  
- Assurer le lien entre utilisateur et logement  

### Relations

- Un **Review est écrit par un seul User**  
- Un **Review est associé à une seule Place**

Cela garantit la traçabilité des avis.

---

## 6. Entité Amenity

La classe `Amenity` représente un équipement disponible dans un logement.

### Attributs principaux

- `name`
- `description`

### Responsabilités

- Définir les équipements disponibles  
- Être associé à plusieurs logements  

### Relations

- Une **Amenity peut être liée à plusieurs Places**  
- Une **Place peut inclure plusieurs Amenities**

Cette relation many-to-many permet la réutilisation des équipements sans duplication.

---

## 7. Justification des relations

Les relations modélisées reflètent la logique métier réelle :

- Les utilisateurs possèdent des logements.  
- Les utilisateurs écrivent des avis.  
- Les avis dépendent des logements.  
- Les équipements sont mutualisés entre plusieurs logements.  

L’héritage via `BaseModel` garantit une structure cohérente.  
Les associations et compositions représentent correctement les dépendances métier.

Cette conception favorise :

- Une forte cohésion  
- Un faible couplage  
- Une bonne maintenabilité  
- Une modélisation métier claire et évolutive  

---

## 8. Visibilités UML

Le diagramme utilise les symboles UML suivants :

- `+` **Public** : accessible depuis l’extérieur  
- `-` **Privé** : accessible uniquement dans la classe  
- `#` **Protégé** : accessible dans la classe et ses sous-classes  

Dans ce modèle :

- Les attributs sont majoritairement **privés (-)** pour garantir l’encapsulation.  
- Les attributs communs de `BaseModel` sont **protégés (#)** pour permettre l’héritage.  
- Les méthodes sont **publiques (+)** afin de définir l’interface de la classe.  

Cela permet de contrôler l’accès aux données et de respecter les principes de la programmation orientée objet.
