from modules.mailSender import sendEmail
from modules.config_reader import Configs

CONFIG_FILENAME = "configs.json"

Configs.load_configs("configs.json")

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
                <th> Total Capacity </th>
    <th> Dose 1 </th><th> Timing </th></tr><tr><td>1</td><td>Chavan Hospital Kandivali West</td><td>No.1 Datta Mandir Rd Opp. L.I.C.Office Kandivali Dahanukar Wadi Kandivali West Mumbai Maharashtra 400067</td><td>61</td><td> 61 </td><td> 10:30:00 - 18:00:00 </td></tr></table></body></html>
"""
subject = "Slots available for label - Test!"

status, error = sendEmail("", subject, mailBody, default=True)

print("Status:", status)
print("Error:", error)
print("Error class:", error.__class__)

if status == 1 and not error:
    print("Test passed")
else:
    print("Test failed")
