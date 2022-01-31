from pyiseers import ERS


def ise_start_connection(
    ers_user,
    ers_pass,
    ise_server='172.28.242.209'):
    '''
    '''
    ise_connection = ERS(
        ise_node=ise_server,
        ers_user=ers_user,
        ers_pass=ers_pass,
        verify=False,
        timeout=10,
        disable_warnings=True
    )
    return ise_connection


def device_details(device_name, ise_connection) -> dict:
    '''
    '''
    return ise_connection.get_device(device_name)['response']


def endpoint_details(
    mac_address,
    ise_connection,
    ticket_id=None) -> dict:
    '''
    '''        
    device = ise_connection.get_endpoint(mac_address)['response']
    if 'not found' in device:
        return {'mac': mac_address, 'id': False, 'ticket_id': ticket_id}
    device['id_group'] = ise_connection.get_endpoint_group(device['groupId'])['response']['name']
    device['ticket_id'] = ticket_id

    return device


def endpoint_groups(ise_connection) -> dict:
    '''
    '''
    return ise_connection.get_endpoint_groups(size=100)['response']


def endpoint_list_details(
    ticket_list,
    ers_user,
    ers_pass,
    ise_server='172.28.242.209') -> dict:
    '''
    '''
    ise_connection = ise_start_connection(ers_user, ers_pass, ise_server)

    ise_endpoint_list = []
    for ticket in ticket_list[:]:
        if ticket['mac']:
            ise_endpoint_list.append(endpoint_details(
                ticket['mac'], ise_connection, ticket_id=ticket['id']))

    return ise_endpoint_list


if __name__ == '__main__':
    pass
