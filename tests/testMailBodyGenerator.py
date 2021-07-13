from modules.mailBodyGenerator import generateMailBody

slots = [[1, 'Chavan Hospital Kandivali West', 'No.1 Datta Mandir Rd Opp. L.I.C.Office Kandivali Dahanukar Wadi Kandivali West Mumbai Maharashtra 400067', 400067, 61, 61, "09-07-2021", '10:30:00 - 18:00:00']]

count = 1

mailBody = generateMailBody(slots, count, 1)

print(mailBody)
