import re
import logging as log
import footprints as foot


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
        'PAL Gaming', project_id)

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


if __name__ == "__main__":
    pass
