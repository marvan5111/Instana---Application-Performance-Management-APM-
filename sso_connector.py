import json
import time
from typing import Dict, Optional
import requests  # Would need to add to requirements.txt

class SSOConnector:
    """SSO connector for OAuth2 and LDAP authentication."""

    def __init__(self, config: Dict):
        self.config = config
        self.oauth_providers = {
            'google': {
                'auth_url': 'https://accounts.google.com/o/oauth2/auth',
                'token_url': 'https://oauth2.googleapis.com/token',
                'userinfo_url': 'https://www.googleapis.com/oauth2/v2/userinfo'
            },
            'github': {
                'auth_url': 'https://github.com/login/oauth/authorize',
                'token_url': 'https://github.com/login/oauth/access_token',
                'userinfo_url': 'https://api.github.com/user'
            }
        }

    def oauth2_login_url(self, provider: str, redirect_uri: str) -> str:
        """Generate OAuth2 login URL for the specified provider."""
        if provider not in self.oauth_providers:
            raise ValueError(f"Unsupported OAuth2 provider: {provider}")

        config = self.oauth_providers[provider]
        params = {
            'client_id': self.config.get(f'{provider}_client_id'),
            'redirect_uri': redirect_uri,
            'scope': 'openid email profile',
            'response_type': 'code',
            'state': self._generate_state()
        }

        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{config['auth_url']}?{query_string}"

    def oauth2_callback(self, provider: str, code: str, redirect_uri: str) -> Optional[Dict]:
        """Handle OAuth2 callback and return user info."""
        if provider not in self.oauth_providers:
            raise ValueError(f"Unsupported OAuth2 provider: {provider}")

        config = self.oauth_providers[provider]

        # Exchange code for access token
        token_data = {
            'client_id': self.config.get(f'{provider}_client_id'),
            'client_secret': self.config.get(f'{provider}_client_secret'),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }

        try:
            token_response = requests.post(config['token_url'], data=token_data)
            token_response.raise_for_status()
            token_info = token_response.json()

            # Get user info
            headers = {'Authorization': f"Bearer {token_info['access_token']}"}
            user_response = requests.get(config['userinfo_url'], headers=headers)
            user_response.raise_for_status()
            user_info = user_response.json()

            return {
                'user_id': user_info.get('id', user_info.get('sub')),
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'provider': provider,
                'access_token': token_info['access_token']
            }
        except Exception as e:
            print(f"OAuth2 callback failed: {e}")
            return None

    def ldap_authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user against LDAP server."""
        # Simplified LDAP authentication (would need ldap3 library)
        ldap_config = self.config.get('ldap', {})

        # Mock LDAP authentication for demo
        if username == 'admin' and password == 'password':
            return {
                'user_id': 'admin',
                'email': 'admin@example.com',
                'name': 'Administrator',
                'groups': ['admin', 'users'],
                'provider': 'ldap'
            }
        elif username == 'viewer' and password == 'password':
            return {
                'user_id': 'viewer',
                'email': 'viewer@example.com',
                'name': 'Viewer User',
                'groups': ['viewer', 'users'],
                'provider': 'ldap'
            }

        return None

    def _generate_state(self) -> str:
        """Generate a random state parameter for OAuth2."""
        import secrets
        return secrets.token_urlsafe(32)

# Global SSO connector instance
sso_connector = SSOConnector({
    'google_client_id': 'demo-client-id',
    'google_client_secret': 'demo-client-secret',
    'github_client_id': 'demo-client-id',
    'github_client_secret': 'demo-client-secret',
    'ldap': {
        'server': 'ldap://localhost:389',
        'base_dn': 'dc=example,dc=com',
        'user_dn': 'cn=users,dc=example,dc=com'
    }
})
