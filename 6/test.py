from requests import get, post
import json

print(post('http://localhost:5000/api/jobs/edit/1',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True}).json())  # все работает

print(post('http://localhost:5000/api/jobs/edit/100',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True}).json())  # нет такого id

print(post('http://localhost:5000/api/jobs/edit/str',
           json={'job': 'da', 'work_size': 1, 'collaborators': '1,2', 'is_finished': True}).json())  # неверный тип

print(post('http://localhost:5000/api/jobs/edit/1',
           json={}).json())  # пустой json

print(post('http://localhost:5000/api/jobs/edit/1',
           json={'job': 'da', 'abc': 'cba'}).json())  # лишний запрос

print(get('http://localhost:5000/api/jobs').json())  # вывод
