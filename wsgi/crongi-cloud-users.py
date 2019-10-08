import urlparse

def application(environ, start_response):
    location = urlparse.parse_qs(environ['QUERY_STRING'])['target']
    status = '302 Redirect'
    output = b'Redirected to {0}'.format(location)

    user = environ['REMOTE_USER']

    response_headers = [('Location', location[0]),]
    start_response(status, response_headers)

    return [output]
