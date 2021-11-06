'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: mailBodyGenerator
Description:
    Accepts slots array and dose number as input and returns an
    HTML table as a string if slots is not empty
----------------------------------------------
'''

def generate_mail_body(slots, dose_number):
    '''
    Inputs: slots(List[List[obj]]), doseNumber(int)
    Description:
        Generates HTML mail body using given slots object
        Returns HTML as a string
    Return:
        status(int), error(Exception object)
    '''
    mail_body = """
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

    if dose_number == 0:
        mail_body += "<th> Dose 1 </th>"
        mail_body += "<th> Dose 2 </th>"
    elif dose_number == 1:
        mail_body += "<th> Dose 1 </th>"
    else:
        mail_body += "<th> Dose 2 </th>"

    mail_body += """
        <th> Fee </th>
        <th> Date </th>
        <th> Timing </th></tr>
    """

    for item in slots:

        slot = f"<tr><td>{item[0]}</td>"
        slot += f"<td>{item[1]}</td>"
        slot += f"<td>{item[2]}</td>"
        slot += f"<td>{item[3]}</td>"
        slot += f"<td>{item[4]}</td>"
        if dose_number == 0:
            slot += f"<td> {item[5]} </td>"
            slot += f"<td> {item[6]} </td>"
            slot += f"<td> {item[7] if item[7] > 0 else 'Free'} </td>"
            slot += f"<td> {item[8]} </td>"
            slot += f"<td> {item[9]} </td>"
        else:
            slot += f"<td> {item[5]} </td>"
            slot += f"<td> {item[6] if item[6] > 0 else 'Free'} </td>"
            slot += f"<td> {item[7]} </td>"
            slot += f"<td> {item[8]} </td>"

        slot += "</tr>"
        mail_body += slot

    mail_body += "</table></body></html>"

    return mail_body
