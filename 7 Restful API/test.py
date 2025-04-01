from requests import get, post, delete

# Проверка users (рабочее)
print(get('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users', json={'name': 'Mark', 'surname': 'Majectic', 'email': 'mark_majectic@mail.py', 'password': 'admin'}).json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(delete('http://localhost:5000/api/v2/users/1').json())

# Проверка users (нерабочее)

# Проверка jobs (рабочее)
print(get('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs', json={'team_leader': 1, 'job': 'купить молоко', 'work_size': 24, 'collaborators': '1,2', 'is_finished': False}).json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(delete('http://localhost:5000/api/v2/jobs/1').json())

# Проверка jobs (нерабочее)

