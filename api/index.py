import sys
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ── UPDATE THESE COOKIES WHEN API STOPS WORKING ──────────────
# How to get fresh cookies:
# 1. Open Chrome on phone/PC
# 2. Go to https://shop2game.com/app/100067/idlogin
# 3. Open DevTools (F12) → Application → Cookies → shop2game.com
# 4. Copy values of: datadome, session_key, _ga, _fbp
COOKIES = {
    '_ga':               'GA1.1.2123120599.1674510784',
    '_fbp':              'fb.1.1674510785537.363500115',
    '_ga_7JZFJ14B0B':   'GS1.1.1674510784.1.1.1674510789.0.0.0',
    'source':            'mb',
    'language':          'en',
    'datadome':          '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
    'session_key':       'efwfzwesi9ui8drux4pmqix4cosane0y',
}
DATADOME_CLIENT_ID = '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0'
# ─────────────────────────────────────────────────────────────

SUPPORTED_REGIONS = {
    'BD':  'Bangladesh',
    'IND': 'India',
    'IN':  'India',
    'SG':  'Singapore',
    'MY':  'Malaysia',
    'ID':  'Indonesia',
    'PK':  'Pakistan',
    'ME':  'Middle East',
    'MA':  'Middle East',
    'BR':  'Brazil',
    'TH':  'Thailand',
    'VN':  'Vietnam',
    'TW':  'Taiwan',
    'RU':  'Russia',
    'CIS': 'CIS',
    'US':  'North America',
}

AUTO_DETECT = ['BD', 'IN', 'SG', 'MA', 'PK', 'ID', 'BR', 'TH', 'VN', 'TW', 'RU', 'CIS', 'US', 'MY']

HEADERS = {
    'Accept-Language':       'en-US,en;q=0.9',
    'Connection':            'keep-alive',
    'Origin':                'https://shop2game.com',
    'Referer':               'https://shop2game.com/app/100067/idlogin',
    'User-Agent':            'Mozilla/5.0 (Linux; Android 11; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    'accept':                'application/json',
    'content-type':          'application/json',
    'sec-ch-ua':             '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile':      '?1',
    'sec-ch-ua-platform':    '"Android"',
    'x-datadome-clientid':   DATADOME_CLIENT_ID,
}


def check_player(uid: str, region: str) -> dict | None:
    cookies = {**COOKIES, 'region': region, 'language': 'ar' if region == 'MA' else 'en'}
    try:
        r = requests.post(
            'https://shop2game.com/api/auth/player_id_login',
            cookies=cookies,
            headers=HEADERS,
            json={'app_id': 100067, 'login_id': uid, 'app_server_id': 0},
            timeout=8,
        )
        if r.status_code == 200:
            d = r.json()
            if d.get('nickname'):
                return d
    except Exception as e:
        print(f'[check_player] {region} error: {e}')
    return None


def check_uid(uid: str, region: str = None) -> dict:
    regions = [region.upper()] if region else AUTO_DETECT

    for r in regions:
        if r not in SUPPORTED_REGIONS:
            return {'status': 'error', 'error': f'Invalid region'}

        data = check_player(uid, r)
        if data:
            return {
                'status':      'success',
                'uid':         uid,
                'nickname':    data.get('nickname'),
                'level':       data.get('level'),
                'region_code': r,
                'region_name': SUPPORTED_REGIONS[r],
            }

    return {'status': 'error', 'error': 'ID NOT FOUND IN SUPPORTED REGIONS'}


@app.route('/')
def home():
    uid    = request.args.get('uid', '').strip()
    region = request.args.get('region', '').strip()
    if not uid:
        return jsonify({
            'name':    'Free Fire UID Checker',
            'usage':   '/?uid=UID or /?uid=UID&region=BD',
            'regions': list(set(SUPPORTED_REGIONS.keys())),
        })
    result = check_uid(uid, region or None)
    return jsonify(result), 200 if result.get('status') == 'success' else 404


@app.route('/xp-opu')
def xp_opu():
    uid    = request.args.get('uid', '').strip()
    region = request.args.get('region', '').strip()
    if not uid:
        return jsonify({'error': 'UID parameter is required'}), 400
    result = check_uid(uid, region or None)
    return jsonify(result), 200 if result.get('status') == 'success' else 404


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


def handler(req, res):
    return app(req, res)
