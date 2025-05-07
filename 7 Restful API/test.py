from requests import get, post, delete, put

# Проверка users (всё рабочее)
print(get('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Mark', 'surname': 'Majectic', 'email': 'mark_majectic@mail.py', 'password': 'admin', 'age': 1,
                 'position': 'abc', 'speciality': 'cba', 'address': '123321'}).json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(delete('http://localhost:5000/api/v2/users/1').json())
print()

# Проверка users (нерабочие)
print(post('http://localhost:5000/api/v2/users', json={}).json())  # подается пустой json
print(post('http://localhost:5000/api/v2/users', json={'name': 'Mark'}).json())  # неполный запрос
print(get('http://localhost:5000/api/v2/users/10').json())  # не существует в таблице
print(delete('http://localhost:5000/api/v2/users/10').json())  # не существует в таблице
print()

# Проверка jobs (всё рабочее)
print(get('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 1, 'job': 'купить молоко', 'work_size': 24, 'collaborators': '1,2',
                 'is_finished': False}).json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(put('http://localhost:5000/api/v2/jobs/1', json={'is_finished': True}).json())
print(delete('http://localhost:5000/api/v2/jobs/1').json())
print()

# Проверка jobs (нерабочие)
print(post('http://localhost:5000/api/v2/jobs', json={}).json())  # подается пустой json
print(post('http://localhost:5000/api/v2/jobs', json={'team_leader': 1}).json())  # неполный запрос
print(get('http://localhost:5000/api/v2/jobs/10').json())  # не существует в таблице
print(put('http://localhost:5000/api/v2/jobs/10', json={'is_finished': True}).json())  # не существует в таблице
print(delete('http://localhost:5000/api/v2/jobs/10').json())  # не существует в таблице
