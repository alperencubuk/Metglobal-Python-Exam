def error_handler():
    try:
        name = int('1232a') # ValueError
        lastname = ['yilmaz', 'keskin'][3] # IndexError
        other_dict = {"name":"merve", "lastname": "demir"}
        other_name = other_dict['other_name'] # KeyError
        age = 1/0 # ZeroDivisionError
        print('OK!')
    except (ValueError, IndexError, KeyError, ZeroDivisionError) as e:
        print(e)

error_handler()

# Alperen Çubuk
