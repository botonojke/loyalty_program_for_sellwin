# How to run a project on your local machine?
1. Install Docker https://docs.docker.com/engine/install/
2. Rename docker-compose_example.yml to docker-compose.yml and dotenv to .env
3. Run `docker-compose up --build`
4. Open http://localhost:8080/browser/ with login: `admin@myapp.com` and password: `mysecretpassword`
5. In pgAdmin, click "Add New Server" and fill in the following details:
    ```
    General > Name: Any name you want to give to the server
    Connection > Host name/address: db
    Connection > Port: 5432
    Connection > Maintenance database: pass
    Connection > Username: sellwin_user
    Connection > Password: sellwin_db
    Click "Save" and you should be able to access your PostgreSQL database through pgAdmin.
    
6. Run migrations by `python manage.py migrate`
7. Run to create admin user `python manage.py createsuperuser` 
8. To load the fixture data into the database, run the loaddata management command `python manage.py loaddata bonus_fixture.json`
9. Run server `python manage.py runserver`
10. Open http://localhost:8080/admin/ in browser and auth with user created at step 9


# How to generate a card?
1. Open http://localhost:8000/card-generator/
2. Fill in the required fields and click generate



