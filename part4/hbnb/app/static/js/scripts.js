/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  let isLogin = checkAuthentication();
  const loginLink = document.getElementById('login-button');
  const logoutLink = document.getElementById('logout-button');
  const loginNav = document.getElementById('login-link');
  if (isLogin) {
    // affiche
    logoutLink.style.display = 'block';
    // masque
    loginLink.style.display = 'none';
    loginNav.style.display = 'none';
  } else {
    loginLink.style.display = 'block';
    loginNav.style.display = 'block';
    logoutLink.style.display = 'none';
  }
  const places_list = document.getElementById('places-list');
  if (places_list) {
    place_list(Infinity);
  };
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', login_submit)
  };
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    if (isLogin) {
      reviewForm.addEventListener('submit', review_submit)
    } else {
      window.location.href = '/index';
    }
  };
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
      priceFilter.addEventListener('change', () => {
        let maxValue = parseInt(document.getElementById('price-filter').value);
        if (isNaN(maxValue)) {
          maxValue = Infinity;
        }
        place_list(maxValue);
    })
  }
  const reviewButton = document.getElementById('add-review');
  if (reviewButton) {
    const button = document.getElementById('add-review-button');
    if (isLogin) {
      button.setAttribute('disabled');
      button.style.cursor = 'pointer';
      button.style.opacity = 1;
    } else {
      button.setAttribute('disabled', 'true');
      button.style.opacity = 0.5;
      const message = document.createElement('p');
      message.textContent = 'You must login to add a review';
      message.classList.add('login-message');
      reviewButton.appendChild(message);
      reviewButton.style.cursor = 'not-allowed';
      button.style.pointerEvents = "none";
    }
  };
});
document.getElementById('logout-button').addEventListener('click', () => logout());

// HOME - List of the places
function place_list (maxValue) {
  document.getElementById('price-filter').addEventListener('change', () => {
        let maxValue = parseInt(document.getElementById('price-filter').value);
        if (isNaN(maxValue)) {
          maxValue = Infinity;
        }
        place_list(maxValue);
    });
  fetch('http://127.0.0.1:5000/api/v1/places/')
      .then(response => response.json())
      .then (data => {
        let places_list = document.getElementById('places-list');
        places_list.textContent = "";
        data.forEach(place => {
          if (maxValue != NaN && place.price <= maxValue) {
            const new_element = document.createElement('div');
            // add title
            const title = document.createElement('h3');
            title.textContent = place.title;
            title.classList.add('place-title');
            new_element.appendChild(title);
            // add description
            const description = document.createElement('p');
            description.textContent = place.description;
            new_element.appendChild(description);
            // add price
            const price = document.createElement('p');
            price.textContent = "Price per night : " + place.price + "$";
            new_element.appendChild(price);
            //add View Detail button
            const details = document.createElement('a');
            details.classList.add('details-button');
            details.href = "/place?id=" + place.id;
            details.textContent = "View Details";
            details.classList.add('view-details-button');
            new_element.appendChild(details);
  
            new_element.classList.add('place-card');
            places_list.appendChild(new_element);
          }
        })
      })
      .catch(error => {
      console.error('Erreur fetch:', error);
    })
}

// LOGIN - send login request
async function login_submit(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: "POST",
      body: JSON.stringify({
        "email": email,
        "password": password
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
    if(response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      document.cookie = `user_id=${data.user_id}; path=/`;
      window.location.href = '/index';
      alert('Welcome back !');
    } else {
      alert('Login failed: ' + response.statusText);
    }
  } catch (error) {
    console.error("Erreur fetch:", error);
  }
}

// REVIEW - send review request
async function review_submit(event) {
  event.preventDefault();
  const review = document.getElementById('review').value;
  const rating = Number(document.getElementById('rating').value);
  const id_data = new URLSearchParams(window.location.search);
  const place_id = id_data.get('id');
  console.log("review:", review);
  console.log("rating:", rating);
  console.log("user_id:", getCookie('user_id'));
  console.log("place_id:", place_id);
  console.log("Authorization:", "Bearer " + getCookie('token'));

  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
      method: "POST",
      body: JSON.stringify({
        "text": review,
        "rating": rating,
        "user_id": getCookie('user_id'),
        "place_id": place_id
      }),
      headers: {
        "Authorization": "Bearer " + getCookie('token'),
        "Content-Type": "application/json"
      }
    })
    if(response.ok) {
      alert('Review submitted successfully !');
      document.getElementById('review').value = "";
      document.getElementById('rating').value = 1;
    } else {
      alert('Failed to submit review');
    }
  } catch (error) {
    console.error("Erreur fetch:", error);
  }
}

function checkAuthentication() {
      const token = getCookie('token');
      if (token) {
        return true;
      } else {
        return false
      };
  }

function getCookie(name) {
    const allCookies = document.cookie.split(';');

    for (let cookie of allCookies) {
      const [key, value] = cookie.trim().split('=');
      if (key === name) {
        return value;
      }
    }
    return null;
}

async function logout() {
  document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  document.cookie = "user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}