import time

a = "16:00:00.000"
b = "16:00:00.000"
c = "16:00:00.000"

def get_sec(time_str):
	h, m, s = time_str.split(':')
	new_result = int(h) * 3600 + int(m) * 60 + float(s)
	new_result += 1.000
	m2, s2 = divmod(new_result, 60)
	h2, m2 = divmod(m2, 60)
	stringeo = "{}:{}:{}".format(int(h2), int(m2), round(s2))
	return stringeo



dif_sec = {'hours': 0, 'minutes': 0, 'seconds': 0}

def str2secs(s):
    h,m,s = map(float,s.split(":"))
    return h*3600+m*60 + s
    

#dif_sec['seconds'] = round((str2secs(a) - str2secs(b)), 3)

# when t1 is greater than t2
if(dif_sec['seconds'] > 0):

	# when is greater than 60 seconds
	if(dif_sec['seconds'] >= 60):
		dif_sec['minutes'], dif_sec['seconds'] = divmod(dif_sec['seconds'], 60)
		dif_sec['seconds'] = round(dif_sec['seconds'], 3)
		result = ("b+{}:{}".format(int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
		print(result)

		# when is greater than 60 minutes
		if(int(dif_sec['minutes']) > 59):
			dif_sec['hours'], dif_sec['minutes'] = divmod(dif_sec['minutes'], 60)
			result = ("c+{}:{}:{}".format(int(dif_sec['hours']), int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
			print(result)

	# when is only about seconds
	else:
		result = 'a+' + str(dif_sec['seconds'])
		print(result)

# when t1 is equal to t2
elif(dif_sec["seconds"] == 0):
	result = str(dif_sec['seconds'])
	print(result)

# when t1 is less than t2
else:

	# when is greater than 60 seconds
	if(dif_sec['seconds'] >= (-60)):
		dif_sec['minutes'], dif_sec['seconds'] = divmod(dif_sec['seconds'], -60)
		dif_sec['seconds'] = round(dif_sec['seconds'], 3)
		result = ("-{}:{}".format(int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
		print(result)

		# when is greater than 60 mintues
		if(int(dif_sec['minutes']) < (-59)):
			dif_sec['hours'], dif_sec['minutes'] = divmod(dif_sec['minutes'], 60)
			result = ("{}:{}:{}".format(int(dif_sec['hours']), int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
			print(result)

	# when is only about seconds
	else:
		result = str(dif_sec['seconds'])
		print(result)

top = 1
while True:

	c = get_sec(c)
	#print("get new time: {}".format(get_sec(c)))
	
	dif_sec['seconds'] = round((str2secs(a) - str2secs(c)), 3)

		# when t1 is greater than t2
	if(dif_sec['seconds'] > 0):
	
		# when is greater than 60 seconds
		if(dif_sec['seconds'] > 59):
			dif_sec['minutes'], dif_sec['seconds'] = divmod(dif_sec['seconds'], 60)
			dif_sec['seconds'] = round(dif_sec['seconds'], 3)
			result = ("b+{}:{}".format(int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
			if(top == 1):
				print(result)
		
	
			# when is greater than 60 minutes
			if(int(dif_sec['minutes']) > 59):
				top = 0
				dif_sec['hours'], dif_sec['minutes'] = divmod(dif_sec['minutes'], 60)
				result = ("c+{}:{}:{}".format(int(dif_sec['hours']), int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
				print(result)

		# when is only about seconds
		else:
			result = 'a+' + str(dif_sec['seconds'])
			print(result)
	
		
	
	# when t1 is equal to t2
	elif(dif_sec["seconds"] == 0):
		result = str(dif_sec['seconds'])
		print(result)
	
	# when t1 is less than t2
	else:
	
		# when t1 is greater than t2
		if(dif_sec['seconds'] < 0):
		
			# when is greater than 60 seconds
			if(dif_sec['seconds'] <= (-60)):
				dif_sec['minutes'], dif_sec['seconds'] = divmod(dif_sec['seconds'], (-60))
				dif_sec['seconds'] = round(dif_sec['seconds'], 3)
				no_sign = str(dif_sec['seconds']).split('-')
				#result = ("b-{}:{}".format(int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
				result = ("b-{}:{}".format(int(dif_sec['minutes']), no_sign[1]))
				if(top == 1):
					print(result)
			
				# when is greater than 60 minutes
				if(int(dif_sec['minutes']) > 59):
					top = 0
					dif_sec['hours'], dif_sec['minutes'] = divmod(dif_sec['minutes'], (60))
					no_sign = str(dif_sec['seconds']).split('-')
					#result = ("c-{}:{}:{}".format(int(dif_sec['hours']), int(dif_sec['minutes']), round(dif_sec['seconds'], 2)))
					result = ("c-{}:{}:{}".format(int(dif_sec['hours']), int(dif_sec['minutes']), no_sign[1]))
					print(result)
	
				# when is only about seconds
			else:
				result = str(dif_sec['seconds']).split('-')
				result = 'a-' + result[1]
				print(result)
	time.sleep(.001)