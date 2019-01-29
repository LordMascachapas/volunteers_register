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
	    if None not in time_event:
		years = time_event[1][0] - time_event[0][0]
		months = time_event[1][1] - time_event[0][1]
		days = time_event[1][2] - time_event[0][2]
		hours = time_event[1][3] - time_event[0][3]
		minutes = time_event[1][4] - time_event[0][4]
		print(str(hours) + 'hours and ' + str(minutes) + 'minutes')
	    else:
		print('Not finished, WORK!!!')
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
	if len(schedules) is not 0:
	    x, y = schedules[-1]
	    if not y:
	        y = date_time
	        schedules[-1] = (x, y)
	    else:
	        schedules.append((date_time, None))
        else:
	    schedules.append((date_time, None))

        users[credentials]["schedules"] = schedules
        write_users_file(users)
    else:
	print("User does not exist")


if __name__ == '__main__':
    start_loop(add_schedule, 0)
