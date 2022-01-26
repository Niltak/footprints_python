'''
First Attempt at a class
'''
import requests
import xmltodict


class Connection(object):
    def __init__(
        self,
        hostname,
        user,
        pwd) -> None:
        '''
        Starts a connection to the foot prints server.
        '''
        self.url = f'https://{hostname}/MRcgi/MRWebServices.pl'
        self.user = user
        self.pwd = pwd


    def requesting(self, data, action):
        '''
        Submits request to the footprints server.
        Returns response.
        '''
        data = data.encode('utf-8')
        headers = {
            'SOAPAction' : f'MRWebServices#MRWebServices__{action}',
            'Content-Type' : 'text/xml; charset=utf-8',
            'Content-Length' : f'{len(data)}'
        }
        return requests.request('POST', self.url, headers=headers, data=data)


    def requesting_dict(self, data, action):
        '''
        Converts requested response to a dictionary for easier manipulation.
        Returns a filtered response
        '''
        response = xmltodict.parse(self.requesting(data, action).text)
        return response['soap:Envelope']['soap:Body'][f'namesp1:MRWebServices__{action}Response']['return']


    def soap_envelope(self, data):
        '''
        Template of the required information around the data requested.
        Returns data inside the template.
        '''
        return f'''
            <SOAP-ENV:Envelope
                xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:namesp2="http://xml.apache.org/xml-soap"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
                    <SOAP-ENV:Header/>
                    <SOAP-ENV:Body>{data}</SOAP-ENV:Body>
            </SOAP-ENV:Envelope>
        '''


    def get_ticket_details(self, project_id, ticket_id):
        '''
        Requests information about a ticket.
        Returns Ticket(class).
        '''
        action = 'getIssueDetails'
        data = f'''
            <namesp1:MRWebServices__{action} xmlns:namesp1="MRWebServices">
                <user xsi:type="xsd:string">{self.user}</user>
                <password xsi:type="xsd:string">{self.pwd}</password>
                <extrainfo xsi:type="xsd:string"/>
                <projectnumber xsi:type="xsd:int">{project_id}</projectnumber>
                <mrid xsi:type="xsd:int">{ticket_id}</mrid>
            </namesp1:MRWebServices__{action}>
        '''
        data = self.soap_envelope(data)
        ticket_dict = self.requesting_dict(data, action)
        if not ticket_dict:
            return False
        
        ticket = Ticket(ticket_id)
        ticket.title = ticket_dict['title']['#text']
        ticket.contact_fullname = f"{ticket_dict['First__bName']['#text']} {ticket_dict['Last__bName']['#text']}"
        ticket.contact_title = ticket_dict['Position__bTitle']['#text']
        ticket.building = ticket_dict['Campus__bBuilding']['#text']
        ticket.status = ticket_dict['status']['#text']
        if '#text' in ticket_dict['description'].keys():
            ticket.details = ticket_dict['description']['#text']
        if '#text' in ticket_dict['Tech__bNotes'].keys():
            ticket.tech_details = ticket_dict['Tech__bNotes']['#text']

        return ticket


    def search_tickets(self, key, project_id):
        '''
        Requests information about a key word in the title of all the tickets.
        Returns a list of Tickets(class).
        '''
        action = 'search'
        query = f"SELECT mrid, mrtitle, mrstatus from MASTER{project_id} WHERE mrtitle LIKE '%{key}%'"
        
        data = f'''
            <namesp1:MRWebServices__{action} xmlns:namesp1="MRWebServices">
                <user xsi:type="xsd:string">{self.user}</user>
                <password xsi:type="xsd:string">{self.pwd}</password>
                <extrainfo xsi:type="xsd:string"/>
                <query xsi:type="xsd:string">{query}</query>
            </namesp1:MRWebServices__{action}>
        '''
        data = self.soap_envelope(data)
        ticket_list_raw = self.requesting_dict(data, action)

        ticket_list = []
        for ticket_raw in ticket_list_raw['item']:
            ticket = Ticket(ticket_raw['mrid']['#text'])
            ticket.title = ticket_raw['mrtitle']['#text']
            ticket.status = ticket_raw['mrstatus']['#text']
            ticket_list.append(ticket)

        return ticket_list


class Ticket(dict):
    def __init__(self, id):
        self.id = id
    
    def info(self):
        '''
        Returns a dictionary of the class.
        '''
        return self.__dict__


if __name__ == "__main__":
    pass