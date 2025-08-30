from jinja2 import Environment, select_autoescape, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def current_user_xml(username: str) -> str:
    template = env.get_template('tests/xml_templates/xml/current_user.xml')
    return template.render({'username': username})


def update_user_xml(uuid: str, username: str, firstname: str = '', surname: str = '', fullname: str = '',
                    currency: str = '', photo: str = '', photo_small: str = '', friendship_status: str = '') -> str:
    template = env.get_template('tests/xml_templates/xml/update_user.xml')
    return template.render({'uuid': uuid,
                            'username': username,
                            'firstname': firstname,
                            'surname': surname,
                            'fullname': fullname,
                            'currency': currency,
                            'photo': photo,
                            'photo_small': photo_small,
                            'friendship_status': friendship_status
                            })


def send_invitation_xml(username: str, to_username: str):
    template = env.get_template('tests/xml_templates/xml/send_invitation.xml')
    return template.render({'from': username, 'to': to_username})


def accept_invitation_xml(username: str, friend: str):
    template = env.get_template('tests/xml_templates/xml/accept_invitation.xml')
    return template.render({'username': username, 'friend': friend})


def decline_invitation_xml(username: str, friend: str):
    template = env.get_template('tests/xml_templates/xml/decline_invitation.xml')
    return template.render({'username': username, 'friend': friend})


def friends(username: str, query: str = ''):
    template = env.get_template('tests/xml_templates/xml/friends.xml')
    return template.render({'username': username, 'query': query})


def remove_friend(username: str, friend: str):
    template = env.get_template('tests/xml_templates/xml/remove_friend.xml')
    return template.render({'username': username, 'friend': friend})