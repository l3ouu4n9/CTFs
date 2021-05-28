import base64


def validate_login(username, password):
    if username != 'admin':
        return False
    
    valid_password = 'QfsFjdz81cx8Fd1Bnbx8lczMXdfxGb0snZ0NGZ'
    return base64.b64encode(password.encode('ascii')).decode('ascii')[::-1].lstrip('=') == valid_password
