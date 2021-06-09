import sqlite3
import requests
import json

url = 'http://127.0.0.1:5000/'
post_data = {'name':'Task 2', 'description':'updated'}

def get_all_items():
	response = requests.get('http://127.0.0.1:5000/api/tasks')
	print(response.text)

def get_item(task_id):
	response = requests.get(f'http://127.0.0.1:5000/api/tasks/{task_id}')
	print(response.text)

def delete_item(task_id):
	response = requests.delete(f'http://127.0.0.1:5000/api/tasks/{task_id}', 
								headers={'Content-Type':'application/json'}
								)
	print(response.text)

def correct_item(task_id, name, description):
	new_data = {'name':name, 
				'description':description
				}
	response = requests.put(f'http://127.0.0.1:5000/api/tasks/{task_id}', 
							data=json.dumps(new_data), 
							headers={'Content-Type':'application/json'}
							)
	print(response.text)

def create_new_item(name, description):
	new_data = {'name':name, 
				'description':description
				}
	response = requests.post('http://127.0.0.1:5000/api/tasks', 
							data=json.dumps(new_data), 
							headers={'Content-Type':'application/json'}
							)
	print(response.text)

def main():
	get_all_items()
	



if __name__ == '__main__':
	main()