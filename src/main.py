from __future__ import print_function

import datetime
from datetime import date
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from src.scrapPage import scrap

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'


def main():
    #Scrap
    provas = scrap()

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Insert events')
    for i in provas:
        events_result = service.events().insert(calendarId='primary', body={"summary": "Prova de " + i.materia,
                                                                            "start": {"date": date(int(i.data.split('/')[2]), int(i.data.split('/')[1]), int(i.data.split('/')[0])).isoformat()},
                                                                            "end": {"date": date(int(i.data.split('/')[2]), int(i.data.split('/')[1]), int(i.data.split('/')[0])).isoformat()},
                                                                            "description": i.professor}).execute()
        print('Event created: %s' % (events_result.get('htmlLink')))


if __name__ == '__main__':
    main()
