import re
import Footprints_Python as foot


def automate_ticket_queue():
    pass


def automate_PAL_Gaming(ticket_id, user, pwd, project_id=17):
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    ticket = foot_connection.get_ticket_details(project_id, ticket_id)
    
    try:
        ticket.info()
    except AttributeError:
        return False

    if 'PAL Gaming' in ticket.title:
        # Tech details or details
        reg_colon = r'&#58;'
        if reg_colon in ticket.tech_details:
            regex_mac1 = fr'..{reg_colon}..{reg_colon}..{reg_colon}..{reg_colon}..{reg_colon}..'
            mac = re.search(regex_mac1, ticket.tech_details).group(0)
            mac = re.sub(reg_colon, ':', mac)
        else:
            regex_mac2 = fr'..-..-..-..-..-..'
            mac = re.search(regex_mac2, ticket.tech_details).group(0)
            mac = re.sub('-', ':', mac)
        return mac

    return False


def search_PAL_Gaming(
    user, pwd, project_id=17, foot_connection=None):

    if not foot_connection:
        foot_connection = foot.Connection(
            'support.purdue.edu', user, pwd)

    ticket_list = foot_connection.search_tickets(
        'PAL Gaming', project_id)

    output_ticket_list = []
    for ticket in ticket_list:
        if ticket.status != 'Closed':
            print(ticket.info())
            output_ticket_list.append(ticket.info())

    if not output_ticket_list:
        return False

    return output_ticket_list


if __name__ == "__main__":
    pass
