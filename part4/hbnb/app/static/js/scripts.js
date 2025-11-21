/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  let isLogin = checkAuthentication();
  const loginLink = document.getElementById('login-button');
  const logoutLink = document.getElementById('logout-button');
  if (isLogin) {
    // affiche
    logoutLink.style.display = 'block';
    // masque
    loginLink.style.display = 'none';
  } else {
    loginLink.style.display = 'block';
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
    const button = document.getElementById('review-button');
    if (isLogin) {
      reviewButton.style.opacity = 1;
      button.href = "/add_review";
    } else {
      reviewButton.style.opacity =  0.6;
      button.style.cursor = 'not-allowed';
      button.href = "";
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
            price.textContent = place.price + "$";
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
      window.location.href = '/index';
      alert('Welcome back !');
    } else {
      alert('Login failed: ' + response.statusText);
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
}