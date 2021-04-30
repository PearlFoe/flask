import random 

population = 'abcdefghijklmnopqrstuvwxyz0123456789'

def generate_key(key_length):
	return ''.join(random.sample(population, key_length))
	