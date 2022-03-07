import footprints_v11 as foot


def ticket_details(user, pwd, project_id, ticket_id):
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    return foot_connection.ticket_details(project_id, ticket_id)


def ticket_search(user, pwd, project_id, key, key_selected='title'):
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    return foot_connection.search_tickets(project_id, key, key_selected=key_selected)


def ticket_create(user, pwd, project_id, title, details):
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    return foot_connection.ticket_create(project_id, title, details)


# def ticket_update(user, pwd, project_id, title, details):
#     foot_connection = foot.Connection(
#         'support.purdue.edu', user, pwd)
#     return foot_connection.ticket_create(project_id, title, details)


def ticket_close(
    user,
    pwd,
    project_id,
    ticket_number,
    resolution='Completed__bSuccessfully',
    assignees=None,
    service_offering='Wired__bCampus__bNetwork__bServices',
    campus='West__bLafayette',
    tech_note='Closed with footprints automation'):
    '''
    '''
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    ticket_return = foot_connection.ticket_close(
        project_id, 
        ticket_number, 
        resolution=resolution,
        assignees=assignees,
        service_offering=service_offering,
        campus=campus,
        tech_note=tech_note)

    return ticket_return


if __name__ == "__main__":
    pass
