from flask import request, jsonify, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

# Initialize Firebase Admin (do this once at top of app.py)
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

@app.route('/google-login', methods=['POST'])
def google_login():
    data = request.get_json()
    id_token = data.get('idToken')

    try:
        # Verify the token server-side
        decoded = firebase_auth.verify_id_token(id_token)

        # Save user info in session
        session['user'] = {
            'uid':   decoded['uid'],
            'email': decoded.get('email'),
            'name':  decoded.get('name'),
        }
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 401
