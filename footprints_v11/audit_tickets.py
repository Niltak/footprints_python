import datetime
import logging as log
import Footprints_Python.footprints_v11 as foot
import nil_lib as ks


def audit_user(
    foot_connection,
    project_id,
    name,
    day_range=365,
    ticket_type=None):
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
            ticket_date = datetime.datetime.strptime(
                ticket.date[:10], '%Y-%m-%d')
            time_diff = datetime.datetime.today() - ticket_date
            if day_range >= time_diff.days:
                if not ticket_type:
                    ticket_list.append(ticket.info())
                    continue
                if ticket.type == 'Incident':
                    ticket_list.append(ticket.info())

    ticket_list = sorted(ticket_list, key=lambda i: i['title'])

    return ticket_list


def audit_network_team(
    user,
    pwd,
    project_id=17,
    day_range=365,
    ticket_type=None,
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
        ticket_list = audit_user(
            foot_connection,
            project_id,
            name,
            day_range=day_range,
            ticket_type=ticket_type)
        team_list.append({'user': name, 'tickets':len(ticket_list), 'ticket_list': ticket_list})

    network_team_numbers = []
    for name in team_list:
        network_team_numbers.append({name['user']: name['tickets']})
    
    team_list = {'user_list': network_team_numbers, 'ticket_details': team_list}

    if not debug:
        ks.file_create(
            f'audit_team_tickets--{datetime.date.today().strftime("%m-%d-%Y")}',
            'logs/audit_tickets/',
            team_list,
            'yml',
        )


if __name__ == "__main__":
    pass
