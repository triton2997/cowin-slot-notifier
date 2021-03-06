'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: mailBodyGenerator
Description:
    Accepts slots array and dose number as input and returns an
    HTML table as a string if slots is not empty
----------------------------------------------
'''

def generateMailBody(slots, doseNumber):
    '''
    Inputs: slots(List[List[obj]]), doseNumber(int)
    Description:
        Generates HTML mail body using given slots object
        Returns HTML as a string
    Return:
        status(int), error(Exception object)
    '''
    mailBody = """
    <html>
        <head>
            <style>
                table {
                    border: 2px solid black;
                    border-collapse: collapse;
                }
                th {
                    text-align: center;
                    background-color: blue;
                    color: white;
                    border: 2px solid black
                }
                td {
                    text-align: center;
                    border: 2px solid black
                }
            </style>
        </head>
    <body>
        <table>
            <tr>
                <th> Sr No </th>
                <th> Name </th>
                <th> Address </th>
                <th> Pincode </th>
                <th> Total Capacity </th>
    """

    if doseNumber == 0:
        mailBody += "<th> Dose 1 </th>"
        mailBody += "<th> Dose 2 </th>"
    elif doseNumber == 1:
        mailBody += "<th> Dose 1 </th>"
    else:
        mailBody += "<th> Dose 2 </th>"

    mailBody += """
        <th> Fee </th>
        <th> Date </th>
        <th> Timing </th></tr>
    """

    for item in slots:

        slot = "<tr><td>{}</td>".format(item[0])
        slot += "<td>{}</td>".format(item[1])
        slot += "<td>{}</td>".format(item[2])
        slot += "<td>{}</td>".format(item[3])
        slot += "<td>{}</td>".format(item[4])
        if doseNumber == 0:
            slot += "<td> {} </td>".format(item[5])
            slot += "<td> {} </td>".format(item[6])
            slot += "<td> {} </td>".format(item[7] if item[7] > 0 else "Free")
            slot += "<td> {} </td>".format(item[8])
            slot += "<td> {} </td>".format(item[9])
        else:
            slot += "<td> {} </td>".format(item[5])
            slot += "<td> {} </td>".format(item[6] if item[6] > 0 else "Free")
            slot += "<td> {} </td>".format(item[7])
            slot += "<td> {} </td>".format(item[8])

        slot += "</tr>"
        mailBody += slot

    mailBody += "</table></body></html>"

    return mailBody
