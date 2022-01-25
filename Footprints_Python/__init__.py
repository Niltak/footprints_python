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
        data = f'''
        <SOAP-ENV:Envelope 
            xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
            xmlns:namesp2="http://xml.apache.org/xml-soap" 
            xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
            xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Header/>
                <SOAP-ENV:Body> 
                    <namesp1:MRWebServices__getIssueDetails xmlns:namesp1="MRWebServices">
                        <user xsi:type="xsd:string">{self.user}</user> 
                        <password xsi:type="xsd:string">{self.pwd}</password> 
                        <extrainfo xsi:type="xsd:string"/> 
                        <projectnumber xsi:type="xsd:int">{project_id}</projectnumber> 
                        <mrid xsi:type="xsd:int">{ticket_id}</mrid> 
                    </namesp1:MRWebServices__getIssueDetails> 
                </SOAP-ENV:Body> 
        </SOAP-ENV:Envelope>
        '''
        action = 'getIssueDetails'

        ticket_dict = self.requesting_dict(data, action)        
        ticket = {
            'title': ticket_dict['title']['#text'],
            'id': ticket_dict['mr']['#text'],
            'contact_fullname': f"{ticket_dict['First__bName']['#text']} {ticket_dict['Last__bName']['#text']}",
            'contact_title': ticket_dict['Position__bTitle']['#text'],
            'building': ticket_dict['Campus__bBuilding']['#text'],
            'status': ticket_dict['status']['#text'],
            # 'building': ticket_dict[]['#text'],
            # 'building': ticket_dict[]['#text'],
        }
        if '#text' in ticket_dict['description'].keys():
            ticket['details'] = ticket_dict['description']['#text']
        if '#text' in ticket_dict['Tech__bNotes'].keys():
            ticket['tech_details'] = ticket_dict['Tech__bNotes']['#text']

        return ticket

    

class Ticket(dict):
    def __init__(self, id):
        self.id = id
    
    def info(self):
        return self.__dict__