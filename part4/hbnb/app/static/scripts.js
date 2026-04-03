/* ============================================================
   SCRIPTS.JS - HBnB Frontend
   ============================================================
   Organisation :
   1. Initialisation (DOMContentLoaded)
   2. Authentification (login, logout, cookie)
   3. Page Index (liste des places + filtres)
   4. Page User (places et reviews de l'utilisateur)
   5. Page Place Details (détail d'une place)
   6. Formulaire Add Review
   ============================================================ */


/* ============================================================
   1. INITIALISATION
   Lance les bonnes fonctions selon la page affichée
   ============================================================ */

document.addEventListener('DOMContentLoaded', async () => {

    /* ----- Formulaire de login ----- */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const emailValue = document.getElementById('email').value;
            const passwordValue = document.getElementById('password').value;
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = '';

            const token = await loginUser(emailValue, passwordValue);

            if (token) {
                /* Sauvegarde le token dans un cookie (valable 1h) */
                document.cookie = 'token=' + token + '; path=/; max-age=3600';
                window.location.href = '/user';
            } else {
                errorMessage.textContent = 'Login failed';
            }
        });
    }

    /* ----- Bouton Login / Logout dans la navbar ----- */
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        if (getCookie('token')) {
            /* Si connecté : on transforme le bouton en "Logout" */
            loginLink.textContent = 'Logout';
            loginLink.addEventListener('click', (event) => {
                event.preventDefault();
                /* Supprime le cookie token pour déconnecter */
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
                window.location.href = '/';
            });
        }
    }

    /* ----- Bouton "My Account" dans la navbar ----- */
    const userLink = document.getElementById('user-link');
    if (userLink) {
        if (getCookie('token')) {
            userLink.style.display = 'inline-block';
        } else {
            userLink.style.display = 'none';
        }
    }

    /* ----- Message de bienvenue sur la page user ----- */
    const welcomeMessage = document.getElementById('welcome-message');
    if (welcomeMessage) {
        const user = await getCurrentUser();
        if (user) {
            welcomeMessage.textContent = 'Welcome ' + user.first_name + ' !';
        }
    }

    /* ----- Lancement selon la page active ----- */

    /* Page Index : affiche la liste des places */
    if (document.getElementById('places-list')) {
        checkAuthentication();
    }

    /* Page User : affiche les places et reviews de l'utilisateur */
    if (document.getElementById('user-places')) {
        loadUserPage();
    }

    /* Page Place Details : affiche le détail d'une place */
    if (document.getElementById('place-details')) {
        loadPlacePage();
    }

    /* Formulaire d'ajout de review (dans la modal de place.html) */
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const token = getCookie('token');
            const placeId = getPlaceIdFromURL();
            const comment = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;

            /* Vérifie que les champs sont remplis */
            if (!comment || !rating) {
                return;
            }

            const response = await submitReview(token, placeId, comment, rating);

            if (response.ok) {
                alert('Review submitted successfully!');
                reviewForm.reset();

                /* Ferme la modal Bootstrap */
                const modal = bootstrap.Modal.getInstance(document.getElementById('Modal'));
                if (modal) {
                    modal.hide();
                }

                /* Recharge les détails de la place pour afficher la nouvelle review */
                await fetchPlaceDetails(token, placeId);
            } else {
                const data = await response.json();
                alert(data.error || 'Failed to submit review');
            }
        });
    }
});


/* ============================================================
   2. AUTHENTIFICATION
   Fonctions liées au login, logout et cookies
   ============================================================ */

/* Envoie les identifiants à l'API et retourne le token si succès */
async function loginUser(email, password) {
    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: password })
    });

    if (response.ok) {
        const data = await response.json();
        return data.access_token;
    } else {
        return false;
    }
}

/* Récupère la valeur d'un cookie par son nom */
function getCookie(name) {
    /* document.cookie retourne tous les cookies sous forme de string "a=1; b=2; c=3" */
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        /* Vérifie si ce cookie commence par le nom recherché */
        if (cookie.startsWith(name + '=')) {
            /* Retourne la valeur après le "=" */
            return cookie.substring((name + '=').length);
        }
    }

    /* Retourne null si le cookie n'existe pas */
    return null;
}

/* Récupère les données de l'utilisateur connecté depuis l'API */
async function getCurrentUser() {
    const token = getCookie('token');

    if (!token) {
        return null;
    }

    const response = await fetch('/api/v1/users/me', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });

    if (response.ok) {
        return await response.json();
    }

    return null;
}


/* ============================================================
   3. PAGE INDEX
   Affiche la liste de toutes les places avec filtres
   ============================================================ */

/* Vérifie l'authentification et lance le chargement des places */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    /* Affiche le login link seulement si pas connecté */
    if (loginLink && !token) {
        loginLink.style.display = 'inline-block';
    }

    fetchPlaces(token);
}

/* Récupère toutes les places depuis l'API */
async function fetchPlaces(token) {
    const headers = { 'Content-Type': 'application/json' };

    /* Ajoute le token dans le header si l'utilisateur est connecté */
    if (token) {
        headers['Authorization'] = 'Bearer ' + token;
    }

    const response = await fetch('/api/v1/places', { method: 'GET', headers: headers });

    if (!response.ok) {
        return;
    }

    const places = await response.json();

    /* Affiche les places et branche les filtres */
    displayPlaces(places);
    setupPriceFilter();
    setupCityFilter();
    setupRatingFilter();
}

/* Crée et affiche les cards des places dans le DOM */
function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) {
        return;
    }

    /* Vide le contenu existant et crée une grille Bootstrap */
    list.innerHTML = '<div class="row row-cols-1 row-cols-md-3 g-4" id="places-row"></div>';
    const row = document.getElementById('places-row');

    for (let i = 0; i < places.length; i++) {
        const place = places[i];

        /* Prépare l'image et le rating à afficher */
        const imgSrc = '/static/' + place.image;
        let ratingDisplay = 'No reviews yet';
        if (place.rating) {
            ratingDisplay = '⭐ ' + place.rating + ' / 5';
        }

        /* Crée l'élément HTML pour cette place */
        const col = document.createElement('div');
        col.className = 'col place-item';

        /* Stocke les données de filtre dans des attributs data-* */
        col.dataset.price = place.price;
        col.dataset.city = place.city || '';
        col.dataset.rating = place.rating || 0;

        col.innerHTML =
            '<div class="card h-100 place-card">' +
                '<img src="' + imgSrc + '" class="card-img-top" alt="' + place.title + '">' +
                '<div class="card-body">' +
                    '<h2 class="card-title">' + place.title + '</h2>' +
                    '<p class="card-text">Price per night: ' + place.price + '€</p>' +
                    '<p class="card-text">' + ratingDisplay + '</p>' +
                    '<a href="/places/' + place.id + '" class="btn details-button">View details</a>' +
                '</div>' +
            '</div>';

        row.appendChild(col);
    }
}

/* Filtre les places affichées selon les trois filtres (prix, ville, rating) */
function filterPlaces() {
    const priceValue = document.getElementById('filter-price').value;
    const cityValue = document.getElementById('filter-city').value;
    const ratingValue = parseFloat(document.getElementById('filter-rating').value || '0');

    /* Récupère toutes les cards de places */
    const items = document.querySelectorAll('.place-item');

    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const itemPrice = parseFloat(item.dataset.price);
        const itemCity = item.dataset.city;
        const itemRating = parseFloat(item.dataset.rating);

        /* Vérifie chaque filtre */
        let priceOk = true;
        if (priceValue) {
            priceOk = itemPrice <= parseFloat(priceValue);
        }

        let cityOk = true;
        if (cityValue) {
            cityOk = itemCity === cityValue;
        }

        const ratingOk = itemRating >= ratingValue;

        /* Affiche ou cache la card selon les filtres */
        if (priceOk && cityOk && ratingOk) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    }
}

/* Branche l'événement change sur le filtre prix */
function setupPriceFilter() {
    const filter = document.getElementById('filter-price');
    if (filter) {
        filter.addEventListener('change', filterPlaces);
    }
}

/* Branche l'événement change sur le filtre ville */
function setupCityFilter() {
    const filter = document.getElementById('filter-city');
    if (filter) {
        filter.addEventListener('change', filterPlaces);
    }
}

/* Branche l'événement change sur le filtre rating */
function setupRatingFilter() {
    const filter = document.getElementById('filter-rating');
    if (filter) {
        filter.addEventListener('change', filterPlaces);
    }
}


/* ============================================================
   4. PAGE USER
   Affiche les places dont l'utilisateur est propriétaire
   et les reviews reçues sur ces places
   ============================================================ */

/* Point d'entrée de la page user */
async function loadUserPage() {
    const token = getCookie('token');

    /* Redirige vers login si pas connecté */
    if (!token) {
        window.location.href = '/login';
        return;
    }

    const user = await getCurrentUser();
    if (!user) {
        return;
    }

    await loadUserPlaces(user.id, token);
}

/* Récupère toutes les places et filtre celles de l'utilisateur */
async function loadUserPlaces(userId, token) {
    const response = await fetch('/api/v1/places', {
        headers: { 'Authorization': 'Bearer ' + token }
    });

    if (!response.ok) {
        return;
    }

    const places = await response.json();

    /* Filtre les places dont owner correspond à l'id de l'utilisateur */
    const userPlaces = [];
    for (let i = 0; i < places.length; i++) {
        if (places[i].owner === userId) {
            userPlaces.push(places[i]);
        }
    }

    displayUserPlaces(userPlaces);
    await loadUserReviews(userPlaces);
}

/* Affiche les cards des places de l'utilisateur */
function displayUserPlaces(places) {
    const container = document.getElementById('user-places');
    if (!container) {
        return;
    }

    if (places.length === 0) {
        container.innerHTML = '<p>You have no places yet.</p>';
        return;
    }

    container.innerHTML = '<div class="row row-cols-1 row-cols-md-3 g-4" id="user-places-row"></div>';
    const row = document.getElementById('user-places-row');

    for (let i = 0; i < places.length; i++) {
        const place = places[i];

        let imgSrc = '/static/images/places/place_default.webp';
        if (place.image) {
            imgSrc = '/static/' + place.image;
        }

        let ratingDisplay = 'No reviews yet';
        if (place.rating) {
            ratingDisplay = '⭐ ' + place.rating + ' / 5';
        }

        const col = document.createElement('div');
        col.className = 'col';
        col.innerHTML =
            '<div class="card h-100 place-card">' +
                '<img src="' + imgSrc + '" class="card-img-top" alt="' + place.title + '">' +
                '<div class="card-body">' +
                    '<h2 class="card-title">' + place.title + '</h2>' +
                    '<p class="card-rating">' + ratingDisplay + '</p>' +
                    '<p class="card-text">Price per night: ' + place.price + '€</p>' +
                    '<a href="/places/' + place.id + '" class="btn details-button">View details</a>' +
                '</div>' +
            '</div>';

        row.appendChild(col);
    }
}

/* Affiche les reviews reçues sur les places de l'utilisateur */
async function loadUserReviews(places) {
    const container = document.getElementById('user-reviews');
    if (!container) {
        return;
    }

    container.innerHTML = '<h2>Reviews on your places</h2>';

    if (places.length === 0) {
        container.innerHTML += '<p>No reviews yet.</p>';
        return;
    }

    /* Pour chaque place, récupère ses reviews */
    for (let i = 0; i < places.length; i++) {
        const place = places[i];

        const response = await fetch('/api/v1/places/' + place.id + '/reviews');
        if (!response.ok) {
            continue;
        }

        const reviews = await response.json();

        /* Passe à la place suivante si pas de reviews */
        if (reviews.length === 0) {
            continue;
        }

        /* Affiche le titre de la place comme séparateur */
        const placeTitle = document.createElement('h3');
        placeTitle.textContent = place.title;
        placeTitle.style.margin = '1.5rem 0 0.5rem 0';
        container.appendChild(placeTitle);

        /* Affiche chaque review */
        for (let j = 0; j < reviews.length; j++) {
            const review = reviews[j];
            const stars = '⭐'.repeat(review.rating);

            /* Récupère le nom de l'auteur */
            let authorName = 'Unknown';
            const userResponse = await fetch('/api/v1/users/' + review.author_id);
            if (userResponse.ok) {
                const author = await userResponse.json();
                authorName = author.first_name + ' ' + author.last_name;
            }

            const card = document.createElement('div');
            card.className = 'review-card';
            card.innerHTML =
                '<div class="card-body">' +
                    '<div class="stars">' + stars + '</div>' +
                    '<p class="author">' + authorName + '</p>' +
                    '<p class="comment">' + review.comment + '</p>' +
                '</div>';

            container.appendChild(card);
        }
    }
}


/* ============================================================
   5. PAGE PLACE DETAILS
   Affiche le détail complet d'une place et ses reviews
   ============================================================ */

/* Extrait l'ID de la place depuis l'URL (ex: /places/abc-123 → "abc-123") */
function getPlaceIdFromURL() {
    const parts = window.location.pathname.split('/');
    return parts[parts.length - 1];
}

/* Point d'entrée de la page place details */
async function loadPlacePage() {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    /* Cache le bouton "Add a review" si pas connecté */
    const addReview = document.getElementById('add-review');
    if (addReview) {
        if (token) {
            addReview.style.display = 'block';
        } else {
            addReview.style.display = 'none';
        }
    }

    await fetchPlaceDetails(token, placeId);
}

/* Récupère les détails d'une place depuis l'API */
async function fetchPlaceDetails(token, placeId) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
        headers['Authorization'] = 'Bearer ' + token;
    }

    const response = await fetch('/api/v1/places/' + placeId, { method: 'GET', headers: headers });
    if (!response.ok) {
        return;
    }

    const place = await response.json();
    await displayPlaceDetails(place);
}

/* Affiche les détails de la place dans le DOM */
async function displayPlaceDetails(place) {

    /* Prépare les données à afficher */
    let imgSrc = '/static/images/places/place_default.webp';
    if (place.image) {
        imgSrc = '/static/' + place.image;
    }

    let ownerName = 'Unknown';
    if (place.owner) {
        ownerName = place.owner.first_name + ' ' + place.owner.last_name;
    }

    let amenities = 'None';
    if (place.amenities && place.amenities.length > 0) {
        const amenityNames = [];
        for (let i = 0; i < place.amenities.length; i++) {
            amenityNames.push(place.amenities[i].name);
        }
        amenities = amenityNames.join(', ');
    }

    /* Calcule la moyenne des ratings */
    let ratingDisplay = 'No reviews yet';
    if (place.reviews && place.reviews.length > 0) {
        let total = 0;
        for (let i = 0; i < place.reviews.length; i++) {
            total += place.reviews[i].rating;
        }
        const avg = (total / place.reviews.length).toFixed(1);
        ratingDisplay = '⭐ ' + avg + ' / 5';
    }

    /* Injecte les infos de la place dans le DOM */
    const placeInfo = document.querySelector('.place-info');
    if (placeInfo) {
        placeInfo.innerHTML =
            '<h1 class="place-title">' + place.title + '</h1>' +
            '<div class="place-media">' +
                '<div class="place-img">' +
                    '<img src="' + imgSrc + '" alt="' + place.title + '">' +
                '</div>' +
                '<div class="place-meta">' +
                    '<p>' + place.description + '</p>' +
                    '<p><strong>Owner :</strong> ' + ownerName + '</p>' +
                    '<p><strong>Price per night :</strong> ' + place.price + '€</p>' +
                    '<p><strong>City :</strong> ' + (place.city || 'Unknown') + '</p>' +
                    '<p><strong>Amenities :</strong> ' + amenities + '</p>' +
                    '<p><strong>Rating :</strong> ' + ratingDisplay + '</p>' +
                '</div>' +
            '</div>';
    }

    /* Met à jour le titre de la modal de review */
    const modalTitle = document.getElementById('ModalLabel');
    if (modalTitle) {
        modalTitle.textContent = 'Reviewing : ' + place.title;
    }

    /* Affiche les reviews */
    const reviewsSection = document.getElementById('reviews');
    if (reviewsSection) {
        reviewsSection.innerHTML = '<h2>Customer reviews</h2>';

        if (!place.reviews || place.reviews.length === 0) {
            reviewsSection.innerHTML += '<p>No reviews yet.</p>';
            return;
        }

        for (let i = 0; i < place.reviews.length; i++) {
            const review = place.reviews[i];
            const stars = '⭐'.repeat(review.rating);

            /* Récupère le nom de l'auteur de la review */
            let authorName = 'Unknown';
            const userResponse = await fetch('/api/v1/users/' + review.author_id);
            if (userResponse.ok) {
                const author = await userResponse.json();
                authorName = author.first_name + ' ' + author.last_name;
            }

            const card = document.createElement('div');
            card.className = 'review-card';
            card.innerHTML =
                '<div class="card-body">' +
                    '<div class="stars">' + stars + '</div>' +
                    '<p class="author">' + authorName + '</p>' +
                    '<p class="comment">' + review.comment + '</p>' +
                '</div>';

            reviewsSection.appendChild(card);
        }
    }
}


/* ============================================================
   6. FORMULAIRE ADD REVIEW
   Envoie une nouvelle review à l'API
   ============================================================ */

/* Envoie la review à l'API et retourne la réponse */
async function submitReview(token, placeId, comment, rating) {
    const response = await fetch('/api/v1/reviews/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({
            comment: comment,
            rating: parseInt(rating),
            place_id: placeId
        })
    });
    return response;
}