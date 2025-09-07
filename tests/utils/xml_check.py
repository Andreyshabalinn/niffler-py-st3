from xml.etree import ElementTree

namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'ns2': 'niffler-userdata'
}


def safe_find_text(element, path, namespaces=None, default=None):
    elem = element.find(path, namespaces)
    return elem.text if elem is not None else default


def check_current_user_result_operation(xml_str: str):
    root = ElementTree.fromstring(xml_str)
    user = root.find('.//ns2:user', namespaces)
    user_data = {
        'id': safe_find_text(user, 'ns2:id', namespaces),
        'username': safe_find_text(user, 'ns2:username', namespaces),
        'fullname': safe_find_text(user, 'ns2:fullname', namespaces),
        'currency': safe_find_text(user, 'ns2:currency', namespaces),
        'friendshipStatus': safe_find_text(user, 'ns2:friendshipStatus', namespaces)
    }
    return user_data


def get_friends_list(xml_str: str):
    root = ElementTree.fromstring(xml_str)
    users = root.find('.//ns2:usersResponse', namespaces)
    return [{
        'id': safe_find_text(user, 'ns2:id', namespaces),
        'username': safe_find_text(user, 'ns2:username', namespaces),
        'currency': safe_find_text(user, 'ns2:currency', namespaces),
        'friendshipStatus': safe_find_text(user, 'ns2:friendshipStatus', namespaces)
    } for user in users]