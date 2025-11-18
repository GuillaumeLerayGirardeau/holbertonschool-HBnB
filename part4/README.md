# HBnB Part 4

This directory contains all the tasks of the HBnB project part 4. You will find down below eplanations about the purpose of all directories and files, a complete description of the core business logic classes, as well as example of uses and instructions to run the application correctly.

## Table of Contents

- [Overall project description](#overall-project-description)
    - [Project Structure](#project-structure)
    - [Run the application](#run-the-application)
- [Core Business Logic Classes](#core-business-logic-classes)
    - [Base Class](#base-class)
    - [User](#user)
    - [Amenity](#amenity)
    - [Place](#place)
    - [Review](#review)
- [Unittest Documentation](#unittest-documentation)
- [Entity Relationship Diagram](#entity-relationship-diagram)
- [Authors](#authors)

## Overall project description

### Project Structure

The HBnB project is composed of several directories and sub-directories, each of them having a precise role in the application's works.
Here is a simple representation of the purpose of each directory :

|   File/Directory       |   Description                                                                                    |
|------------------------|--------------------------------------------------------------------------------------------------|
| `app/`                 | Contains the core application code.                                                              |
| `api/`                 | Houses the API endpoints, organized by version.                                                  |
| `models/`              | Contains the business logic classes.                                                             |
| `services/`            | Implements the Facade pattern to manage interaction between layers.                              |
| `persistence/`         | Contains the in-memory repository; will later be replaced by a SQL Alchemy-based solution.       |
| `run.py`               | Entry point for running the Flask application.                                                   |
| `config.py`            | Used for configuring environment variables and application settings.                             |
| `requirements.txt`     | Lists all the Python packages required for the project.                                          |
| `README.md`            | Provides a brief overview of the project.                                                        |
### Run the application

To run properly the HBnB application, be sure to follow these steps correctly :
- Install the required packages contained in *requirements.txt* :
````
pip install -r requirements.txt
````
- Run the application by executing *run.py* :
````
python3 run.py
````
This project use Python3, you may want to have a similar version of Python to avoid errors.

## Core Business Logic Classes

In the *models* folder, you can found all the different entities that compose the core of the HBnB website. You can found down below the description of each of them, with a representation of their attributes, methods and relationships.

### Base Class

This entity contains all attributes and methods that will be the common ground of all the other entities. Every following classes will inherit from *Base Class*.

- **Attributes**

| Name         | Type       | Description                                                            |
|--------------|------------|------------------------------------------------------------------------|
| `id`         | `UUID`     | A unique identifier (UUID) automatically generated for each instance   |
| `created_at` | `datetime` | Timestamp indicating when the object was created                       |
| `updated_at` | `datetime` | Timestamp indicating the last time the object was updated              |

- **Methods**

| Name            | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `save()`        | Updates the `updated_at` timestamp to the current time                      |
| `update(data)`  | Updates the object's attributes using a dictionary                          |

### User

This entity define user's data and actions in the HBnB website.

- **Attributes**

| Name           | Type       | Description                                                                 |
|----------------|------------|-----------------------------------------------------------------------------|
| `first_name`   | `str`      | User's first name.                                                          |
| `last_name`    | `str`      | User's last name.                                                           |
| `email`        | `str`      | User's email address.                                                       |
| `is_admin`     | `bool`     | Indicates whether the user has administrative privileges.                   |
| `places`       | `list`     | List of places belonging to the user.                                       |
| `reviews`      | `list`     | List of reviews submitted by the user.                                      |

- **Methods**

| Name               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `add_places(place)`| Adds a place to the user's places list.                                     |
| `add_reviews(review)`| Adds a review to the user's reviews list.                                 |

- **Relationships**

| Related Entity | Relationship Type | Description |
|--------------------|-----------------------|------------------|
| `Place`            | One-to-Many           | A user can add multiple places|
| `Review`           | One-to-Many           | A user can add multiple reviews|

- **Example and usage**
````
# import the User class
from app.models.user import User

# create a user
user1 = User("Alice", "Dupont", "alice.dupont@example.com", is_admin=False)

# adding a place
user1.add_places("Holberton School")

# adding a review
user1.add_reviews("Great School !")
````

### Amenity

This entity define places's features such as Wi-Fi or TV.

- **Attributes**

| Attribute   | Type   | Description                                                  |
|-------------|--------|--------------------------------------------------------------|
| `name`      | `str`  | The name of the amenity.                                     |
| `places`    | `list` | A list of places that offer this amenity.                    |

- **Methods**

| Method         |Description                                                   |
|----------------|--------------------------------------------------------------|
| `add_place(place)`    | Adds a place to the `places` list.                           |

- **Relationships**

| Related Entity     | Relationship Type     | Description |
|--------------------|-----------------------|------------------|
| `Place`            | Many-to-Many           | An amenity can be linked to multiple places that include this feature, and a place can have multiple amenities|

- **Example and usage**
````

# import the Amenity class
from app.models.amenity import Amenity

# create an amenity
wifi = Amenity("Wi-Fi")

# adding a place
wifi.add_place("Holberton School")
````

### Place

This entity define places' informations and adress, and contains owner's information as well as all the amenities it has.

- **Attributes**

| Attribute     | Type     | Description                                                                 |
|---------------|----------|-----------------------------------------------------------------------------|
| `title`       | `str`    | The title of the place.                                                     |
| `description` | `str`    | Description of the place.                                                   |
| `price`       | `float`  | Cost of the place.                                                          |
| `latitude`    | `float`  | Geographic latitude of the place.                                           |
| `longitude`   | `float`  | Geographic longitude of the place                                           |
| `owner_id`    | `str`    | Identifier of the user who owns the place.                                  |
| `amenities`   | `list`   | A list of amenities associated with the place.                              |
| `reviews`     | `list`   | A list of reviews submitted for the place.                                  |

- **Methods**

| Name               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `add_review(review)`| Adds a review to the `reviews` list.                                     |
| `add_amenity(amenity)`| Adds an amenity to the `amenities` list.                                  |

- **Relationships**

| Related Entity | Relationship Type | Description                                                                 |
|----------------|-------------------|-----------------------------------------------------------------------------|
| `Amenity`      | Many-to-Many      | A place can have multiple amenities. An amenity can be assigned to multiple places.|
| `Review`       | One-to-Many       | A place can receive multiple reviews.                                       |
| `User`         | Many-to-One       | Each place is owned by a single user.                                       |


- **Example and usage**
````
# import the Place class
from app.models.place import Place

# create a place
place1 = Place(
    title="Holberton School",
    description="A great school to learn Python",
    price=7450.0,
    latitude=48.117,
    longitude=-1.677,
    owner_id="01b254561r1238754"
)

# adding an amenity
place1.add_amenity("Free Wi-Fi")

# adding a review
place1.add_review("Loved the coffee")
````
### Review

This entity define review that can be assigned to places by the users of the application.

- **Attributes**

| Attribute   | Type     | Description                                           |
|-------------|----------|-------------------------------------------------------|
| `text`      | `str`    | The content of the review.                            |
| `rating`    | `int`    | The rating given by the user.                         |
| `place`     | `Place`  | The id of the place being reviewed.                   |
| `user`      | `User`   | The id of the user who submitted the review.          |

- **Relationships**

| Related Entity | Relationship Type | Description                                           |
|----------------|-------------------|-------------------------------------------------------|
| `Place`        | Many-to-One       | Each review is linked to one place.                   |
| `User`         | Many-to-One       | Each review is submitted by one user.                 |


- **Example and usage**
````
# import the Review class
from app.models.review import Review

# create a review
review1 = Review(
    text="Amazing School !",
    rating=5,
    place="fgdd8efsdsaz54tyuiok1bv",
    user="rhjiko5l423kn6fd45y"
)
````
## Unittest Documentation

The following documentation is a spreadsheat of the expectations and results of the different tests we use on our code.
In the last column you can see the actual result we have for the test of this row, so if a test is not working you can see it there.

# User unittest documentation

| Test Name                         | Description                                     | Sent Data                                                                                   | Expected Result      | Actual Result      |
|----------------------------------|-------------------------------------------------|---------------------------------------------------------------------------------------------|----------------------|--------------------|
| test_create_user                 | Create a user with valid data                   | first_name, last_name, email, is_admin                                                      | 201 Created          | 201 Created        |
| test_create_user_invalid_first_name | Create a user with empty first name         | first_name: "", last_name, email, is_admin                                                  | 400 Bad Request      | 400 Bad Request    |
| test_create_user_invalid_last_name  | Create a user with empty last name          | first_name, last_name: "", email, is_admin                                                  | 400 Bad Request      | 400 Bad Request    |
| test_create_user_invalid_email      | Create a user with malformed email           | first_name, last_name, email: "invalid-email", is_admin                                     | 400 Bad Request      | 400 Bad Request    |
| test_create_user_invalid_is_admin   | Create a user with invalid is_admin type     | first_name, last_name, email, is_admin: ""                                                  | 400 Bad Request      | 400 Bad Request    |
| test_get_user                    | Retrieve all users                             | None                                                                                        | 200 OK               | 200 OK             |
| test_get_user_by_id             | Retrieve a user by valid ID                   | user_id                                                                                     | 200 OK               | 200 OK             |
| test_get_user_by_id_invalid_id  | Retrieve a user by invalid ID                 | user_id: "azerty123456"                                                                     | 404 Not Found        | 404 Not Found      |
| test_update_user                | Update a user with valid data                 | first_name, last_name, email, is_admin                                                      | 200 OK               | 200 OK             |
| test_update_user_invalid_id     | Update a user with invalid ID                 | user_id: "azerty123456", valid fields                                                       | 404 Not Found        | 404 Not Found      |
| test_update_user_invalid_first_name | Update with empty first name               | first_name: "", last_name, email, is_admin                                                  | 400 Bad Request      | 400 Bad Request    |
| test_update_user_invalid_last_name  | Update with empty last name                | first_name, last_name: "", email, is_admin                                                  | 400 Bad Request      | 400 Bad Request    |
| test_update_user_invalid_email      | Update with invalid email                  | first_name, last_name, email: "not_an_email", is_admin                                      | 400 Bad Request      | 400 Bad Request    |
| test_update_user_invalid_is_admin   | Update with invalid is_admin value         | first_name, last_name, email, is_admin: "not_a_bool"                                        | 400 Bad Request      | 400 Bad Request    |


# Place unittest documentation

| Test Name                              | Description                                           | Sent Data                                                                                             | Expected Result   | Actual Result     |
|---------------------------------------|-------------------------------------------------------|--------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| test_create_places                    | Create a place with valid data                        | title, description, price, latitude, longitude, owner_id                                               | 201 Created       | 201 Created       |
| test_create_invalid_place_title       | Create place with empty title                         | title: "", other fields valid                                                                          | 400 Bad Request   | 400 Bad Request   |
| test_create_invalid_place_description | Create place with empty description                   | description: "", other fields valid                                                                    | 400 Bad Request   | 400 Bad Request   |
| test_create_invalid_place_price       | Create place with negative price                      | price: -52.0, other fields valid                                                                       | 400 Bad Request   | 400 Bad Request   |
| test_create_invalid_place_latitude    | Create place with invalid latitude (> 90 or < -90)    | latitude: 237.7749                                                                                     | 400 Bad Request   | 400 Bad Request   |
| test_create_invalid_place_longitude   | Create place with invalid longitude (> 180 or < -180) | longitude: -5122.4194                                                                                  | 400 Bad Request   | 400 Bad Request   |
| test_create_invalid_place_owner       | Create place with empty owner_id                      | owner_id: ""                                                                                           | 400 Bad Request   | 400 Bad Request   |
| test_create_place_invalid_owner_id    | Create place with non-existing owner_id               | owner_id: "azerty123456"                                                                               | 400 Bad Request   | 400 Bad Request   |
| test_get_all_place                    | Retrieve all places                                   | None                                                                                                   | 200 OK            | 200 OK            |
| test_get_place_by_id                  | Retrieve place by valid ID                            | place.id                                                                                               | 200 OK            | 200 OK            |
| test_get_place_by_id_invalid_id       | Retrieve place with invalid ID                        | place.id: "azerty123456"                                                                               | 404 Not Found     | 404 Not Found     |
| test_update_place                     | Update place with valid data                          | title, description, price                                                                              | 200 OK            | 200 OK            |
| test_update_place_invalid_title       | Update place with empty title                         | title: "", valid description & price                                                                   | 400 Bad Request   | 400 Bad Request   |
| test_update_place_invalid_description | Update place with empty description                   | description: "", valid title & price                                                                   | 400 Bad Request   | 400 Bad Request   |
| test_update_place_invalid_price       | Update place with negative price                      | price: -200.0, valid title & description                                                                | 400 Bad Request   | 400 Bad Request   |
| test_update_place_invalid_id          | Update non-existing place                             | place.id: "azerty123456", valid fields                                                                 | 404 Not Found     | 404 Not Found     |
| test_add_new_amenity                  | Add an existing amenity to a place                    | amenity name: "Pool", valid place.id                                                                   | 200 OK            | 200 OK            |
| test_add_new_amenity_invalid_amenity_name | Add a non-existent amenity to a place           | amenity name: "Garden", not created beforehand                                                         | 404 Not Found     | 404 Not Found     |
| test_add_new_amenity_invalid_input    | Add amenity with wrong input field                    | json: {"data": "Pool"}                                                                                 | 400 Bad Request   | 400 Bad Request   |
| test_add_new_amenity_invalid_place_id | Add amenity to invalid place                          | place.id: "azerty123456", amenity name: "Free Wi-fi"                                                   | 404 Not Found     | 404 Not Found     |


# Amenity unittest documentation

| Test Name                        | Description                                  | Sent Data                          | Expected Result   | Actual Result     |
|----------------------------------|----------------------------------------------|-------------------------------------|-------------------|-------------------|
| test_create_amenities           | Create an amenity with valid data            | name: "Wi-Fi"                       | 201 Created       | 201 Created       |
| test_create_invalid_amenity     | Create an amenity with empty name            | name: ""                            | 400 Bad Request   | 400 Bad Request   |
| test_get_all_amenity            | Retrieve all amenities                       | None                                | 200 OK            | 200 OK            |
| test_get_amenity_by_id          | Retrieve amenity by valid ID                 | amenity.id                          | 200 OK            | 200 OK            |
| test_get_amenity_by_id_invalid_id | Retrieve amenity with invalid ID           | amenity.id: "azerty123456"          | 404 Not Found     | 404 Not Found     |
| test_update_amenity             | Update amenity with valid name               | name: "TV"                          | 200 OK            | 200 OK            |
| test_update_amenity_invalid_name| Update amenity with empty name               | name: ""                            | 400 Bad Request   | 400 Bad Request   |
| test_update_amenity_invalid_id  | Update non-existing amenity by ID           | amenity.id: "azerty123456", name: "TV" | 404 Not Found  | 404 Not Found     |


# Review unittest documentation

| Test Name                          | Description                                            | Sent Data                                                                                      | Expected Result                   | Actual Result      |
|-----------------------------------|--------------------------------------------------------|------------------------------------------------------------------------------------------------|-----------------------------------|--------------------|
| test_create_review                | Create a valid review                                  | text, rating (5), user_id, place_id                                                            | 201 Created                       | 201 Created        |
| test_create_invalid_review_text   | Create review with empty text                          | text: "", rating: 5, user_id, place_id                                                         | 400 Bad Request                   | 400 Bad Request    |
| test_create_invalid_review_rating | Create review with invalid rating (out of range)       | text, rating: 9, user_id, place_id                                                             | 400 Bad Request                   | 400 Bad Request    |
| test_create_invalid_review_user   | Create review with invalid user ID                     | text, rating: 5, user_id: "azerty123456", place_id                                             | 404 Not Found                     | 404 Not Found      |
| test_create_invalide_review_place | Create review with invalid place ID                    | text, rating: 5, user_id, place_id: "azerty123456"                                             | 404 Not Found                     | 404 Not Found      |
| test_get_all_reviews              | Retrieve all reviews                                   | None                                                                                           | 200 OK                            | 200 OK             |
| test_get_review_by_id             | Retrieve review by valid ID                            | review.id                                                                                      | 200 OK                            | 200 OK             |
| test_get_review_by_invalid_id     | Retrieve review by invalid ID                          | review_id: "azerty123456"                                                                      | 404 Not Found                     | 404 Not Found      |
| test_update_review                | Update review with valid data                          | review.id, text: "Amazing stay!", rating: 4                                                    | 200 OK                            | 200 OK             |
| test_update_review_invalid_text   | Update review with empty text                          | review.id, text: "", rating: 4                                                                 | 400 Bad Request                   | 400 Bad Request    |
| test_update_review_invalid_rating | Update review with invalid rating                      | review.id, text: "Amazing stay!", rating: 10                                                   | 400 Bad Request                   | 400 Bad Request    |
| test_update_review_invalid_id     | Update review with invalid ID                          | review_id: "azerty123456", text: "Amazing stay!", rating: 4                                    | 404 Not Found                     | 404 Not Found      |
| test_delete_review                | Delete a review with valid ID                          | review.id                                                                                      | 200 OK                            | 200 OK             |
| test_delete_review_invalid_id     | Delete a review with invalid ID                        | review_id: "azerty123456"                                                                      | 404 Not Found                     | 404 Not Found      |
| test_get_reviews_by_place         | Get reviews by valid place ID                          | place.id                                                                                       | 200 OK                            | 200 OK             |
| test_get_reviews_by_place_invalid_id | Get reviews by invalid place ID                     | place_id: "azerty12346"                                                                        | 404 Not Found                     | 404 Not Found      |

## Entity Relationship Diagram

<img width="624" height="1305" alt="Heir diagram" src="https://github.com/user-attachments/assets/93bb34d0-b308-47cf-83ef-de9508e629dc" />

## Authors

- [@niimatik](https://github.com/niimatik)
- [@GuillaumeLerayGirardeau](https://github.com/GuillaumeLerayGirardeau)
