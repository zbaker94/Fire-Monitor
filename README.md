# Fire Monitor
Listen to changes to a firebase document. Useful for updating settings on an IOT device.

The script.py requires a settings.json in the same directory as the script. If not present, the file will be created.

It also requires you to setup a service account for your project. The process to create the service account (and download the credentials json) can be found here https://cloud.google.com/docs/authentication/getting-started
Once done, place your credentials.json (renaming if needed) in the same folder as listen.py

Be sure to export the file as per the instructions above before running.
