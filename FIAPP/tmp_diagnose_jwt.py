import os
import json
import traceback
from google.oauth2 import service_account
from google.auth.transport.requests import Request


def main():
    path = os.getenv('FIREBASE_CREDENTIALS_PATH')
    print('FIREBASE_CREDENTIALS_PATH ->', path)
    if not path or not os.path.exists(path):
        print('ERROR: cred file not found at path above')
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        print('ERROR: could not parse JSON credentials (bad format/encoding)')
        traceback.print_exc()
        return

    print('client_email ->', data.get('client_email'))
    pk = data.get('private_key')
    if not pk:
        print('ERROR: private_key not present in JSON')
        return

    print('private_key present ->', pk.strip().startswith('-----BEGIN PRIVATE KEY-----'))
    print('private_key length ->', len(pk))

    # Try to refresh an access token directly
    try:
        scopes = [
            'https://www.googleapis.com/auth/firebase.database',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/cloud-platform',
        ]
        creds = service_account.Credentials.from_service_account_file(path, scopes=scopes)
        req = Request()
        print('Attempting to refresh credentials (this triggers JWT grant)')
        creds.refresh(req)
        print('Refresh succeeded. token:', creds.token)
        print('Expiry:', creds.expiry)
    except Exception:
        print('Refresh failed — traceback:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
