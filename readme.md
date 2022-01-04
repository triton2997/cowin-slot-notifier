Co-WIN slot notifier

## Overview

A tool built for automatically checking and notifying the user of slots available on CoWIN portal.

The search feature on the portal allows users to search only based on state and district or pincode.

This tool allows us to filter on multiple parameters like vaccine type, dose number, free/paid, and also allows user to specify of a list of pincodes to filter on.

The tool continuously checks for slots with a set interval by hitting the CoWIN public APIs, and sends an email whenever a slot is found. Currently, slots are checked for the current and next date


Developed as a personal project. Any suggestions and improvements are welcome! :)

## Project description
#### Project structure
cowin-slot-notifier

| files

| -- configs.json

| -- credentials.json

| -- params.json

| logs

| modules

| -- config_reader.py

| -- cowin_slots_finder.py

| -- mail_body_generator.py

| -- mail_sender.py

| -- params_reader.py

| tests

| main.py

### Flow:
1. Configs file is read and a Configs object is created. This object contains tool configurations like file names, check intervals, mail host, port, credentials, etc.
2. Params file is read and a list of dictionaries is returned. Params file is a JSON file containing a parameter configuration for each label (Each unique configuration we want to check slots for)
3. CoWIN APIs are checked for each parameter dictionary. If slots are found after applying all the filters, list of lists is returned
4. If slots are found, mail body with an HTML table is generated and returned as a string
5. The generated mail body is sent to the email configured in the parameter configuration. The from address is used from the credentials JSON file

### Module descriptions:

1. config_reader.py - Reads configs.json and creates a Configs object
2. params_reader.py - Reads the params file and returns a list of dictionaries, one for each parameter configuration
2. cowin_slots_finder.py - Hits CoWIN APIs and returns available slots as a list of lists
3. mail_body_generator.py - Generates the mail body using the slots object
4. mail_sender.py - Sends the email once slots are found


## Setup

## Config descriptions

## Release Notes
