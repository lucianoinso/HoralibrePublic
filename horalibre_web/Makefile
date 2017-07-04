run:
	python manage.py runserver

clean:
	rm */*.pyc
	rm -rf records/migrations
	rm -rf commentary/migrations
	rm -rf login/migrations
	rm -rf administration/migrations

update_models:
	python manage.py makemigrations "login" "records" "commentary" "administration"
	python manage.py migrate

# Para crear un nuevo proyecto:
# django-admin startproject project_name

# Para crear una nueva app
# python manage.py startapp app_name

# Crear
# q = Goal(goal_text="TEST", finish_date=timezone.now())
# q.save()

# Crear
# user = User(username="fran", password="fran", mail="fran")
# user.save()
# user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
