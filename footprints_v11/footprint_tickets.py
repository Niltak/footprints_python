import footprints_v11 as foot


def ticket_details(user, pwd, project_id, ticket_id):
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    return foot_connection.get_ticket_details(project_id, ticket_id)


def ticket_search(user, pwd, key, project_id):
    foot_connection = foot.Connection(
        'support.purdue.edu', user, pwd)
    return foot_connection.search_tickets(key, project_id)


if __name__ == "__main__":
    pass
