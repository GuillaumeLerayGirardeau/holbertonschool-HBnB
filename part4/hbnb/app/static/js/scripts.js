/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => place_list());
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', login_submit)
    }
});
document.getElementById('price-filter').addEventListener('change', (event) => price_filter(event));

// HOME - List of the places
function place_list () {
    fetch('http://127.0.0.1:5000/api/v1/places/')
      .then(response => response.json())
      .then (data => {
        places_list = document.getElementById('places-list');
        data.forEach(place => {
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

          details.addEventListener('click', () => show_place_details(place.id))

          new_element.classList.add('place-card');
          places_list.appendChild(new_element);
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
