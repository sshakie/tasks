from requests import get, post, delete
import json


print(post('http://localhost:5000/api/jobs',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True}).json(), '+')  # все работает


print(get('http://localhost:5000/api/jobs').json(), '+') # правильно
print(get('http://localhost:5000/api/jobs/1').json(), '+') # правильно
print(get('http://localhost:5000/api/jobs/10').json(), '-')  # нет такого
print(get('http://localhost:5000/api/jobs/a').json(), '-')  # неверный тип


print(post('http://localhost:5000/api/jobs',
           json={'job': 'da', 'work_size': 1}).json(), '-')  # не хватает обязательного компонента
print(post('http://localhost:5000/api/jobs',
           json={}).json(), '-')  # пустой json
print(post('http://localhost:5000/api/jobs',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True,
                 'abc': 'cba'}).json(), '-')  # лишний запрос


print(post('http://localhost:5000/api/jobs/edit/1',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True}).json(), '+')  # все работает
print(post('http://localhost:5000/api/jobs/edit/100',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True}).json(), '-')  # нет такого id
print(post('http://localhost:5000/api/jobs/edit/str',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True}).json(), '-')  # неверный тип
print(post('http://localhost:5000/api/jobs/edit/1',
           json={}).json(), '-')  # пустой json
print(post('http://localhost:5000/api/jobs/edit/1',
           json={'job': 'da', 'abc': 'cba'}).json(), '-')  # лишний запрос
print(get('http://localhost:5000/api/jobs').json(), '+')  # вывод

