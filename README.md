# Code challenge

The objective of this code challenge is to develop a backend service or api.

I am developing an Api for CRUD operations over Restaurant objects.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. To get the server running you just need to run the docker-compose up command from the top level directory of the project.

```
docker-compose up
```

It is possible that the `web` container finishes loading up before the `db` container. In this case a message like the one below will appear.

> web_1  | psycopg2.OperationalError: could not connect to server: Connection refused
> web_1  | 	Is the server running on host "db" (172.18.0.2) and accepting
> web_1  | 	TCP/IP connections on port 5432?

To fix this simply `ctrl + c` and `docker-compose up` again. Now the server should be running on `localhost:8000`.

Once the server is up and running make sure to run the migrations by doing:

```
docker-compose web run python3 manage.py migrate
```

The api is now available on `localhost:8000/restaurants/`. Check the documentation below for the detailed method description.

## API Documentation

**List Restaurants**
----

* **URL**

  `r'^restaurants/$'`

* **Method:**
  
  `GET`

* **Success Response:**
  * **Code:** 200 <br />
    **Content:**

```
    [
        {
            id : 1,
            name: 'Restaurant 1',
            opens_at: '12:00',
            closes_at: '13:00'
        }, {
            id : 2,
            name: 'Restaurant 2',
            opens_at: '12:00',
            closes_at: '13:00'
        }
    ]
```

**Create Restaurant**
----

* **URL**

  `r'^restaurants/$'`

* **Method:**
  
  `POST`
  
* **Data Params**

```
    {
        name: 'Restaurant x'
        opens_at: '12:00'
        closes_at: '16:00'
    }
```

* **Success Response:**
  * **Code:** 201 CREATED <br />
    **Content:** `{ id : new id }`
 
* **Error Response:**
  * **Code:** 400 BAD REQUEST <br />

**Restaurant Details**
----

* **URL**

  `r'^restaurants/(?P<pk>[0-9]+)/$'`

* **Method:**

  `GET`
  
*  **URL Params**
   **Required:**
 
   `pk=[integer]`

* **Success Response:**
  * **Code:** 200 OK <br />
    **Content:**

```
    {
        id: pk,
        name: 'Restaurant',
        opens_at: '12:00',
        closes_at: '16:00' 
    }
```
 
* **Error Response:**
  * **Code:** 404 NOT FOUND <br />

**Delete Restaurant**
----

* **URL**

  `r'^restaurants/(?P<pk>[0-9]+)/$'`

* **Method:**

  `DELETE`
  
*  **URL Params**
   **Required:**
 
   `pk=[integer]`

* **Success Response:**
  * **Code:** 204 NO CONTENT <br />
 
* **Error Response:**
  * **Code:** 404 NOT FOUND <br />

**Update Restaurant**
----

* **URL**

  `r'^restaurants/(?P<pk>[0-9]+)/$'`

* **Method:**

  `PUT`
  
*  **URL Params**
   **Required:**
 
   `pk=[integer]`

* **Data Params**

```
    {
        name: 'New Restaurant name'
        opens_at: '12:00'
        closes_at: '16:00'
    }
```

* **Success Response:**
  * **Code:** 200 <br />
    **Content:** 

```
    {
        name: 'New Restaurant name'
        opens_at: '12:00'
        closes_at: '16:00'
    }
```

* **Error Response:**
  * **Code:** 400 BAD REQUEST <br />

  OR

  * **Code:** 404 NOT FOUND <br />

## Built With

* [Docker](https://www.docker.com/) - For containerizing the application
* [Django 2.0](https://www.djangoproject.com/) - The web framework used
* [PostgreSQL](https://www.postgresql.org/) - For data persistence
