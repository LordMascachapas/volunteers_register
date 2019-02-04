import datetime
import json
from reader import start_loop

def show_schedules():
    users = read_users_file()
    for user in users:
	user_data = users.get(user)
	print(user_data.get("name"))
	print(' - schedules:')
	for time_event in user_data.get("schedules"):
	    if time_event.get('end'):
		years = time_event['end'][0] - time_event['start'][0]
		months = time_event['end'][1] - time_event['start'][1]
		days = time_event['end'][2] - time_event['start'][2]
		hours = time_event['end'][3] - time_event['start'][3]
		minutes = time_event['end'][4] - time_event['start'][4]
		print(str(hours) + ' hours and ' + str(minutes) + ' minutes')
		if years > 0:
		    print('   + WARNING this work shift has taken ' + str(years) + ' years')
		elif months > 0:
		    print('   + WARNING this work shift has taken ' + str(months) + ' months')
		if days > 0:
		    print('   + WARNING this work shift has taken ' + str(days) + ' days')
	    else:
		print('Not finished ... WORK !!!')
	print('\n ------------- \n')

def write_users_file(log_data):
    with open("users.json", "w") as outfile:
	json.dump(log_data, outfile)
	outfile.close()


def read_users_file():
    with open("users.json", "r") as outfile:
	dir = json.load(outfile)
	return dir


def authenticate_user(credentials):
    user = read_users_file().get(credentials)
    return user, credentials


def new_user_entry(credentials):
    user, credentials = authenticate_user(credentials)
    if not user:
	name = raw_input("Name: ")
	users = read_users_file()
	users[credentials] = {"name": name, "schedules": []}
	write_users_file(users)
    else:
	print("User already exists")


def add_user():
    start_loop(new_user_entry, 1)


def add_schedule(credentials):
    users = read_users_file()
    user, credentials = authenticate_user(credentials)
    if user:
	now = datetime.datetime.now()
	date_time = (now.year, now.month, now.day, now.hour, now.minute)
	schedules = user.get("schedules")
	if len(schedules) is 0 or schedules[-1].get('end'):
	    schedules.append({'start': date_time, 'end': None})
	    print('work shift started ...')
	else:
	    schedules[-1]['end'] = date_time
	    print('work shift done :)')

        users[credentials]["schedules"] = schedules
        write_users_file(users)
    else:
	print("User does not exist")
