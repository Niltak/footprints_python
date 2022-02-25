import re
import yaml
import logging as log
import footprints_v11 as foot


def automate_ticket_queue():
    pass


def automate_PAL_Gaming(
    ticket_id,
    user,
    pwd,
    project_id=17,
    foot_connection=None):
    '''
    '''
    if not foot_connection:
        foot_connection = foot.Connection(
            'support.purdue.edu', user, pwd)
    ticket = foot_connection.ticket_details(project_id, ticket_id)
    
    try:
        ticket.info()
    except AttributeError:
        return False

    if 'PAL Gaming'.lower() in ticket.title.lower():
        if hasattr(ticket, 'tech_notes') and hasattr(ticket, 'full_notes'):
            ticket.full_notes = ticket.full_notes + ticket.tech_notes
        elif not hasattr(ticket, 'full_notes'):
            ticket.full_notes = ticket.tech_notes

        reg_colon = r'&#58;'
        regex_mac1 = fr'..{reg_colon}..{reg_colon}..{reg_colon}..{reg_colon}..{reg_colon}..'
        regex_mac2 = fr'..-..-..-..-..-..'
        mac = False
        try: 
            mac = re.search(regex_mac1, ticket.full_notes).group(0)
            mac = re.sub(reg_colon, ':', mac)
        except Exception:
            pass
        try:
            mac = re.search(regex_mac2, ticket.full_notes).group(0)
            mac = re.sub('-', ':', mac)
        except Exception:
            pass

        return {'id': ticket.id, 'mac': mac}


def search_PAL_Gaming(
    user,
    pwd,
    project_id=17,
    foot_connection=None,
    debug=None):
    '''
    '''
    if not foot_connection:
        foot_connection = foot.Connection(
            'support.purdue.edu', user, pwd)

    ticket_list = foot_connection.search_tickets(
        project_id, 'PAL Gaming')

    output_ticket_list = []
    for ticket in ticket_list:
        if ticket.status != 'Closed':
            if debug:
                print(ticket.info())
            output_ticket_list.append(ticket)

    if not output_ticket_list:
        return False

    return output_ticket_list


def automate_PAL_Gaming_tickets(
    user,
    pwd,
    project_id=17,
    debug=None):
    '''
    '''
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    
    try:
        ticket_list = search_PAL_Gaming(
            user, pwd, foot_connection=foot_connection)
    except:
        log.debug('No new tickets found!')
        return False

    ticket_mac_list = []
    for ticket in ticket_list:
        ticket_details = automate_PAL_Gaming(
            ticket.id, user, pwd, foot_connection=foot_connection)
        ticket_mac_list.append(ticket_details)
    
    return ticket_mac_list


def audit_user(
    foot_connection,
    project_id,
    name):
    '''
    '''
    try:
        full_ticket_list = foot_connection.search_tickets(
            project_id, name, key_selected='assignee')
    except:
        log.debug('No new tickets found!')
        return False

    ticket_list = []
    for ticket in full_ticket_list:
        if ticket.status == 'Closed' or ticket.status == 'Resolved':
            if '2022-' in ticket.date or '2021-' in ticket.date and not '2021-01' in ticket.date:
                if ticket.type == 'Incident':
                    ticket_list.append(ticket.info())

    ticket_list = sorted(ticket_list, key=lambda i: i['title'])

    return ticket_list


def audit_network_team(
    user,
    pwd,
    project_id=17,
    debug=None):
    '''
    '''
    network_team = [
        'kvsampso',
        'skfoley',
        'dekkyb',
        'peercy',
        'richar96',
        'mskvarek',
        'montgo59',
        'huffb',
        'caseb',
        'rolanda',
        'jandres',
        'jone1513',
        'jehimes']

    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    team_list = []
    for name in network_team:
        ticket_list = audit_user(foot_connection, project_id, name)
        team_list.append({'user': name, 'tickets':len(ticket_list), 'ticket_list': ticket_list})

    network_team_numbers = []
    for name in team_list:
        network_team_numbers.append({name['user']: name['tickets']})
    
    team_list = {'user_list': network_team_numbers, 'ticket_details': team_list}
    with open('audit_team_tickets.yml', 'w') as data_file:
        data_file.writelines(yaml.dump(team_list, sort_keys=False))


if __name__ == "__main__":
    pass
