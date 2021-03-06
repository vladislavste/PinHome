from flask import request, jsonify, current_app
from functools import wraps
from authorization.models import User
from rauth import OAuth1Service, OAuth2Service
from flask import url_for, redirect, request, session
from flask_jwt import JWT, jwt_required, current_identity
import json
import jwt


def token_check(function_to_decorate):
    @wraps(function_to_decorate)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'There is not token'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query \
                .filter_by(token=data['public_id']) \
                .first()
            if not current_user:
                raise
        except:
            return jsonify({
                'message': 'Token incorrect'
            }), 401
        # returns the current logged in users contex to the routes
        return function_to_decorate(current_user.token, *args, **kwargs)

    return decorated


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('authorization.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('me?fields=id,email').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email')
        )


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://oauth2.googleapis.com/token',
            base_url='https://www.googleapis.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('oauth2/v2/userinfo').json()
        return (
            'google$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email')
        )


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__('yandex')
        self.service = OAuth2Service(
            name='yandex',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.yandex.ru/authorize',
            access_token_url='https://oauth.yandex.ru/token',
            base_url='https://login.yandex.ru/info'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('').json()
        return (
            'yandex',
            me['id'],
            me['login']
        )