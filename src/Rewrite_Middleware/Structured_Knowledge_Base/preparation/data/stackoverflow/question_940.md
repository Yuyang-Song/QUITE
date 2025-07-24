# Django REST Framework - overriding JSONWebTokenAuthentication for custom JWT authentication
[Link to question](https://stackoverflow.com/questions/51078756/django-rest-framework-overriding-jsonwebtokenauthentication-for-custom-jwt-aut)
**Creation Date:** 1530176465
**Score:** 1
**Tags:** django, authentication, jwt
## Question Body
<p>I have a Django application with external database, which means that for every user request I'm sending SQL queries to external DB server. No local DB (like sqllite or such) exists. Also, JWT should be used to authenticate users.
To do so, I've overwritten <code>ObtainJSONWebToken</code> view:</p>

<pre><code>class ObtainJWT(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # verify that user with given credentials exist in db
        resp = requests.post(settings.SERVER_HOST+"/auth/",
                             json={"username":username, "password":password})
        if resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response({'error':'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # create token
        payload = jwtutils.jwt_payload_handler(username, password, api_settings.JWT_EXPIRATION_DELTA)
        token = jwt_encode_handler(payload)
        return Response({'token': token},
                        status=status.HTTP_200_OK)
</code></pre>

<p>And <code>jwt_payload_handler</code> in <code>jwtutils</code>:</p>

<pre><code>def jwt_payload_handler(username, password, delta):
    # custom payload handler
    payload = {
        'username': username,
        'password': password,
        'exp': datetime.utcnow() + delta
    }

    return payload
</code></pre>

<p>Now I can successfully obtain token without using any <code>User</code> objects. But when obtained token is used (a user tries to access protected routes with the token), <code>{"detail":"Invalid signature."}</code> is returned. I think it's because DRF's <code>JSONWebTokenAuthentication</code> class that I'm using has <code>authenticate_credentials</code> method that checks if a user with given credentials exists in local DB ( <a href="https://github.com/GetBlimp/django-rest-framework-jwt/blob/master/rest_framework_jwt/authentication.py#L59" rel="nofollow noreferrer">https://github.com/GetBlimp/django-rest-framework-jwt/blob/master/rest_framework_jwt/authentication.py#L59</a> ), hence the error. So I decided to create custom authentication class.
There is what I wrote:</p>

<pre><code>class JSONWebTokenAuthentication(BaseAuthentication):
"""
Token based authentication using the JSON Web Token standard.
"""
def get_jwt_value(self, request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

    if not auth:
        if api_settings.JWT_AUTH_COOKIE:
            return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
        return None

    if smart_text(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        msg = _('Invalid Authorization header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) &gt; 2:
        msg = _('Invalid Authorization header. Credentials string '
                'should not contain spaces.')
        raise exceptions.AuthenticationFailed(msg)

    return auth[1]

def authenticate(self, request):
    """
    Returns a two-tuple of `User` and token if a valid signature has been
    supplied using JWT-based authentication.  Otherwise returns `None`.
    """
    jwt_value = self.get_jwt_value(request)
    if jwt_value is None:
        return None

    try:
        payload = jwt_decode_handler(jwt_value)
    except jwt.ExpiredSignature:
        msg = ('Signature has expired.')
        raise exceptions.AuthenticationFailed(msg)
    except jwt.DecodeError:
        msg = _('Error decoding signature.')
        raise exceptions.AuthenticationFailed(msg)
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed()

    return (None, payload)
</code></pre>

<p>However, that doesn't work. I'm returning <code>None</code> instead of a valid <code>User</code> object. Somewhere later in Django's authentication process that value is read and tested if it's <code>is_authenticated()</code> returns <code>True</code>. Returning <code>None</code> would obviously result in <code>{"detail":"You do not have permission to perform this action."}</code>.</p>

<p>I'm relatively new to Django and JWT, what is the best way to rewrite the authentication class so I'd be able not to have any Django<code>User</code>s saved locally and not break anything in Django authentication process? Or maybe I need to rewrite some permissions classes? Thanks in advance.</p>

## Answers
### Answer ID: 54927561
<p>Not sure if you solved this but did you add your custom authentication class in rest framework settings? something like this:</p>

<pre><code>  REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'myapp.location.JSONWebTokenAuthentication' #location of your custom authentication class.
        ),
    }
</code></pre>

