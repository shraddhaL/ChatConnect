# ChatConnect

Steps to setup this project in your local machine:

1. You need to have MySQL installed
2. Create a schema named 'chatapp'. You can use below query.
   ```python
   CREATE SCHEMA `chatapp` ;
   ```
4. Create and apply migrations
   You can use below commands
   ```python
    python manage.py makemigrations
    python manage.py migrate
   ```
   If these commands do not work, you can use the ones below. Also, I recommend to drop and re-create the schema
   ```python
   DROP SCHEMA `chatapp` ;
   CREATE SCHEMA `chatapp` ;
   ```
   Then on the terminal run
   ```python
    python manage.py makemigrations users
    python manage.py migrate users
    python manage.py makemigrations groupchat
    python manage.py migrate groupchat
    python manage.py makemigrations
    python manage.py migrate
   ```
6. Load the Data for admin user with below command.
   ```python
    python manage.py loaddata initial_data
   ```
8. To test the application run
   ```python
    python manage.py test
   ```

Admin User:

username: admin

password: admin
