# 📘 Explanatory Notes – Version Française

## 1. Architecture générale

L’application **HBnB** est structurée selon une architecture en trois couches (*layered architecture*).  
Cette organisation permet de séparer clairement les responsabilités, de réduire le couplage entre les composants et de faciliter la maintenance ainsi que l’évolution du système.

Les trois couches principales sont :

- **Presentation Layer**
- **Business Logic Layer**
- **Persistence Layer**

Chaque couche possède un rôle précis et communique uniquement avec la couche immédiatement inférieure.

---

## 2. Presentation Layer

La couche **Presentation** constitue le point d’entrée de l’application.  
Elle est responsable de l’interaction avec les utilisateurs via des endpoints API.

### Responsabilités principales

- Recevoir les requêtes HTTP  
- Extraire et valider le format des données entrantes  
- Gérer les codes de réponse HTTP  
- Transmettre les demandes à la couche Business Logic  

Cette couche ne contient aucune règle métier.  
Elle ne connaît pas la structure interne des modèles ni les mécanismes de stockage des données.  
Son rôle est purement orienté communication et exposition des services.

La séparation garantit que toute modification de la logique métier ou de la base de données n’impacte pas directement l’API.

---

## 3. Business Logic Layer

La couche **Business Logic** représente le cœur fonctionnel de l’application.

### Elle contient :

- Les modèles métier (`User`, `Place`, `Review`, `Amenity`)  
- Les règles de validation métier  
- Les cas d’usage (`RegisterUser`, `CreatePlace`, `SubmitReview`, etc.)  
- La façade (point d’entrée interne)  

### Responsabilités

- L’application des règles métier  
- La cohérence des données  
- L’orchestration des opérations  
- La coordination entre modèles et persistence  

Elle ne dépend pas de la couche Presentation et ne connaît pas les détails techniques de la base de données.

La logique métier est centralisée ici afin de garantir la cohérence du système et d’éviter la duplication de règles dans d’autres couches.

---

## 4. Persistence Layer

La couche **Persistence** est chargée du stockage et de la récupération des données.

### Elle comprend :

- Les repositories (`UserRepository`, `PlaceRepository`, etc.)  
- Les mécanismes d’accès à la base de données (SQL, ORM, DAO)  

### Responsabilités

- Exécuter les opérations CRUD  
- Gérer les requêtes SQL  
- Assurer la communication avec la base de données  
- Encapsuler les détails techniques liés au stockage  

Cette couche isole totalement la logique métier des détails d’implémentation de la base de données.

Grâce à cette séparation, il est possible de changer de technologie de stockage sans modifier la Business Logic.

---

## 5. Rôle du Facade Pattern

Le **Facade Pattern** est utilisé pour simplifier la communication entre la Presentation Layer et la Business Logic Layer.

### La façade :

- Fournit un point d’entrée unique  
- Expose des méthodes de haut niveau  
- Masque la complexité interne  
- Réduit le couplage entre les couches  

Sans façade, la couche Presentation devrait interagir directement avec plusieurs modèles ou cas d’usage, ce qui augmenterait la dépendance et la complexité.

Grâce à la façade :

- La Presentation ne connaît qu’une interface unique  
- La Business Logic conserve le contrôle total de son organisation interne  
- Les modifications internes n’impactent pas l’API  

La façade améliore donc la maintenabilité, la lisibilité et la robustesse de l’architecture.

---

## 6. Communication entre les couches

Le flux de communication est strictement unidirectionnel :

Presentation → Business Logic (via Facade)
Business Logic → Persistence (via Repositories)


Aucune couche ne doit accéder directement à une couche non adjacente.

Cette organisation garantit :

- Une forte cohésion interne  
- Un faible couplage externe  
- Une architecture évolutive  
- Une meilleure testabilité  

---

# 📘 Explanatory Notes – English Version 

## 1. Overall Architecture

The **HBnB application** follows a three-layered architecture.  
This structure ensures clear separation of responsibilities, reduced coupling, and improved maintainability and scalability.

The three main layers are:

- **Presentation Layer**
- **Business Logic Layer**
- **Persistence Layer**

Each layer has a clearly defined responsibility and communicates only with the adjacent layer.

---

## 2. Presentation Layer

The **Presentation Layer** serves as the entry point of the application.  
It handles user interaction through API endpoints.

### Responsibilities

- Receiving HTTP requests  
- Validating input format  
- Managing HTTP response codes  
- Forwarding requests to the Business Logic layer  

This layer does not contain business rules.  
It does not access the database directly nor manipulate domain models.

Its purpose is strictly to expose services and manage communication between the client and the system.

---

## 3. Business Logic Layer

The **Business Logic Layer** represents the core of the application.

### It contains:

- Domain models (`User`, `Place`, `Review`, `Amenity`)  
- Business validation rules  
- Use cases (`RegisterUser`, `CreatePlace`, `SubmitReview`, etc.)  
- The Facade (internal entry point)  

### Responsibilities

- Applying business rules  
- Ensuring data consistency  
- Orchestrating operations  
- Coordinating between models and persistence  

It remains independent from the Presentation Layer and does not depend on database implementation details.

Centralizing business logic in this layer ensures system consistency and avoids duplication of rules.

---

## 4. Persistence Layer

The **Persistence Layer** is responsible for data storage and retrieval.

### It includes:

- Repositories (`UserRepository`, `PlaceRepository`, etc.)  
- Database access mechanisms (SQL, ORM, DAO)  

### Responsibilities

- Executing CRUD operations  
- Managing SQL queries  
- Handling communication with the database  
- Encapsulating storage-related technical details  

This isolation allows the Business Logic to remain independent of database technology.

As a result, the storage solution can be changed without affecting business logic.

---

## 5. Role of the Facade Pattern

The **Facade Pattern** simplifies communication between the Presentation and Business Logic layers.

### The facade:

- Provides a single entry point  
- Exposes high-level methods  
- Hides internal complexity  
- Reduces coupling between layers  

Without the facade, the Presentation Layer would need to directly interact with multiple models or services, increasing complexity and dependency.

By using a facade:

- The Presentation Layer interacts with one unified interface  
- The internal organization of the Business Layer remains protected  
- Internal changes do not affect the API layer  

This improves maintainability, readability, and architectural robustness.

---

## 6. Layer Communication Flow

The communication flow is strictly unidirectional:

Presentation → Business Logic (via Facade)
Business Logic → Persistence (via Repositories)


No layer directly accesses a non-adjacent layer.

This structure ensures:

- High cohesion  
- Low coupling  
- Scalability  
- Better testability  
