import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SUPPORTED_REGIONS = {
    'BD':  'Bangladesh',
    'IND': 'India',
    'SG':  'Singapore',
    'MY':  'Malaysia',
    'ID':  'Indonesia',
    'PK':  'Pakistan',
    'ME':  'Middle East',
    'BR':  'Brazil',
    'TH':  'Thailand',
    'VN':  'Vietnam',
    'TW':  'Taiwan',
    'RU':  'Russia',
    'CIS': 'CIS',
    'US':  'North America',
    'NA':  'North America',
}

AUTO_DETECT = ['BD', 'IND', 'SG', 'ID', 'PK', 'ME', 'BR', 'TH', 'VN', 'TW', 'RU', 'CIS', 'US', 'MY']

# Multiple Garena shop endpoints — try all until one works
ENDPOINTS = [
    'https://shop.garena.my/api/auth/player_id_login',
    'https://shop2game.com/api/auth/player_id_login',
    'https://shop.garena.sg/api/auth/player_id_login',
]

HEADERS = {
    'User-Agent':      'Mozilla/5.0 (Linux; Android 13; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Accept':          'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type':    'application/json',
    'Origin':          'https://shop.garena.my',
    'Referer':         'https://shop.garena.my/app/100067/idlogin',
    'X-Requested-With': 'com.garena.myshop',
}


def query_endpoint(url: str, uid: str, region: str) -> dict | None:
    try:
        s = requests.Session()
        s.cookies.set('region',   region)
        s.cookies.set('language', 'en')
        s.cookies.set('source',   'mb')
        r = s.post(url, headers=HEADERS,
                   json={'app_id': 100067, 'login_id': uid, 'app_server_id': 0},
                   timeout=7)
        if r.status_code == 200:
            d = r.json()
            if d.get('nickname'):
                return d
    except:
        pass
    return None


def check_uid(uid: str, region: str = None) -> dict:
    regions = [region.upper()] if region else AUTO_DETECT

    for r in regions:
        if r not in SUPPORTED_REGIONS:
            return {'status': 'error', 'error': f'Invalid region. Supported: {", ".join(SUPPORTED_REGIONS)}'}

        for endpoint in ENDPOINTS:
            data = query_endpoint(endpoint, uid, r)
            if data:
                return {
                    'status':      'success',
                    'uid':         uid,
                    'nickname':    data.get('nickname'),
                    'level':       data.get('level'),
                    'region_code': r,
                    'region_name': SUPPORTED_REGIONS[r],
                }

    return {'status': 'error', 'error': 'Player not found in any region'}


@app.route('/')
@app.route('/api')
def home():
    uid    = request.args.get('uid', '').strip()
    region = request.args.get('region', '').strip()
    if not uid:
        return jsonify({
            'name':    'Free Fire UID Checker API',
            'version': '2.0.0',
            'usage':   '/?uid=YOUR_UID or /?uid=YOUR_UID&region=BD',
            'regions': list(SUPPORTED_REGIONS.keys()),
        })
    result = check_uid(uid, region or None)
    return jsonify(result), 200 if result['status'] == 'success' else 404


@app.route('/api/check')
def check():
    uid    = request.args.get('uid', '').strip()
    region = request.args.get('region', '').strip()
    if not uid:
        return jsonify({'error': 'uid is required'}), 400
    result = check_uid(uid, region or None)
    return jsonify(result), 200 if result['status'] == 'success' else 404


@app.route('/api/health')
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'version': '2.0.0'})


# Vercel entry point
def handler(req, res):
    return app(req, res)
