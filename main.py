# CoWIN slot notifier using CoWIN public APIs
# Gets details from a props file (* is required)
    # District ID*
    # Date*
    # Email ID*
    # Fee type
    # Min Age
    # Pincode list
    # vaccine
    # dose number
# Gets slots available based on above filters
# Sends email to the email ID specified above


from cowinSlotsFinder import findAvailability
from mailBodyGenerator import generateMailBody
from mailSender import sendEmail
from configPropertiesReader import getConfigProperties

CONFIG_FILENAME = 'config.xml'

props = getConfigProperties(CONFIG_FILENAME)

for prop in props:
    slots, count = findAvailability(prop)

    if count == -1:
        subject = "Invalid state/district configured for label - {}".format(prop["label"])
        mailBody = """Invalid state/district configured. Please update the state/district
        State: {}
        District: {}
        """.format(prop["state"], prop["district"])

    else:
        mailBody = generateMailBody(slots, count, 1)
        subject = ""
        if count > 0:
            subject = "Slots available for label - {}!".format(prop["label"])
        else:
            subject = "Sorry, no slots available right now"

    sendEmail(prop["email_id"], subject, mailBody)