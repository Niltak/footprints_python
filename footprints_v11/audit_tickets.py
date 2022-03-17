import yaml
import logging as log
import footprints_v11 as foot


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
            if ('2022-' in ticket.date or '2021-' in ticket.date) and not '2021-01' in ticket.date and not '2021-02' in ticket.date:
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
