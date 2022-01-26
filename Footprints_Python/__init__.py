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
        
        self.url = f'https://{hostname}/MRcgi/MRWebServices.pl'
        self.user = user
        self.pwd = pwd


    def requesting(self, data, action):
        '''
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
        '''
        # might require below in the furture
        # list(reponse['soap:Envelope']['soap:Body'].keys())[0]
        reponse = xmltodict.parse(self.requesting(data, action).text)
        return reponse['soap:Envelope']['soap:Body'][f'namesp1:MRWebServices__{action}Response']['return']


    def get_ticket_details(self, project_id, ticket_id):
        '''
        '''
        action = 'getIssueDetails'
        data = f'''
        <SOAP-ENV:Envelope
            xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:namesp2="http://xml.apache.org/xml-soap"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Header/>
                <SOAP-ENV:Body>
                    <namesp1:MRWebServices__{action} xmlns:namesp1="MRWebServices">
                        <user xsi:type="xsd:string">{self.user}</user>
                        <password xsi:type="xsd:string">{self.pwd}</password>
                        <extrainfo xsi:type="xsd:string"/>
                        <projectnumber xsi:type="xsd:int">{project_id}</projectnumber>
                        <mrid xsi:type="xsd:int">{ticket_id}</mrid>
                    </namesp1:MRWebServices__{action}>
                </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>
        '''

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
        '''
        action = 'search'
        query = f"SELECT mrid, mrtitle, mrstatus from MASTER{project_id} WHERE mrtitle LIKE '%{key}%'"
        # query = f"SELECT * FROM *"
        data = f'''
        <SOAP-ENV:Envelope
            xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:namesp2="http://xml.apache.org/xml-soap"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Header/>
                <SOAP-ENV:Body>
                    <namesp1:MRWebServices__{action} xmlns:namesp1="MRWebServices">
                        <user xsi:type="xsd:string">{self.user}</user>
                        <password xsi:type="xsd:string">{self.pwd}</password>
                        <extrainfo xsi:type="xsd:string"/>
                        <query xsi:type="xsd:string">{query}</query>
                    </namesp1:MRWebServices__{action}>
                </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>
        '''
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
        return self.__dict__


if __name__ == "__main__":
    pass