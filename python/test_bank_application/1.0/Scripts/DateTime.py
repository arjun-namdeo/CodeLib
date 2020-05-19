def CurrentDateTime ():
    import datetime
    Date = str(datetime.datetime.now())
    time = ' AM'
    Month = ""
    if int((Date.split(' ')[1]).split(':')[0])>12:
        time = ' PM'
    Month_Int = str(Date.split(' ')[0]).split('-')[1]
    
    Dict = {1:"Jan", 2:"Feb", 3:"March", 4:"April",
            5:"May", 6:"June", 7:"July", 8:"Aug",
            9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec",}

    Month =  str(Dict[int(Month_Int)])


    SetDate = str(Date.split(' ')[0]).split('-')[2] + ' ' +  str(Month) + ' '+ str(Date.split(' ')[0]).split('-')[0]
    SetCurrentDateTime = str(SetDate) +  ' at ' + (Date.split(' ')[1]).split(':')[0] +':' + (Date.split(' ')[1]).split(':')[1] + str(time)

    return (SetCurrentDateTime)