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
}

AUTO_DETECT_ORDER = ['BD', 'IND', 'SG', 'ID', 'PK', 'ME', 'BR', 'TH', 'VN', 'TW', 'RU', 'CIS', 'US', 'MY']

HEADERS = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection':      'keep-alive',
    'Origin':          'https://shop2game.com',
    'Referer':         'https://shop2game.com/app/100067/idlogin',
    'User-Agent':      'Mozilla/5.0 (Linux; Android 11; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    'accept':          'application/json',
    'content-type':    'application/json',
}


def get_player(uid: str, region: str) -> dict | None:
    """Call shop2game API for a specific region."""
    try:
        # Get fresh session cookies first
        session = requests.Session()
        session.headers.update({'User-Agent': HEADERS['User-Agent']})
        session.get('https://shop2game.com/app/100067/idlogin', timeout=6)
        session.cookies.set('region',   region)
        session.cookies.set('language', 'en')
        session.cookies.set('source',   'mb')

        r = session.post(
            'https://shop2game.com/api/auth/player_id_login',
            headers=HEADERS,
            json={'app_id': 100067, 'login_id': uid, 'app_server_id': 0},
            timeout=8,
        )
        if r.status_code == 200:
            data = r.json()
            if data.get('nickname'):
                return data
    except Exception as e:
        print(f'[get_player] {region} error: {e}')
    return None


def check_uid(uid: str, region: str = None) -> dict:
    regions = [region.upper()] if region else AUTO_DETECT_ORDER

    for r in regions:
        if r not in SUPPORTED_REGIONS:
            return {'status': 'error', 'error': f'Invalid region. Supported: {", ".join(SUPPORTED_REGIONS.keys())}'}

        data = get_player(uid, r)
        if data and data.get('nickname'):
            return {
                'status':      'success',
                'uid':         uid,
                'nickname':    data.get('nickname'),
                'level':       data.get('level'),
                'region_code': r,
                'region_name': SUPPORTED_REGIONS[r],
            }

    return {'status': 'error', 'error': 'Player not found in any region'}


# ── Routes ────────────────────────────────────────────────────

@app.route('/')
@app.route('/api')
def home():
    uid    = request.args.get('uid')
    region = request.args.get('region')

    if not uid:
        return jsonify({
            'name':    'Free Fire UID Checker API',
            'version': '1.0.0',
            'usage':   '/?uid=YOUR_UID',
            'optional':'&region=BD',
            'regions': list(SUPPORTED_REGIONS.keys()),
        })

    result = check_uid(uid, region)
    code   = 200 if result.get('status') == 'success' else 404
    return jsonify(result), code


@app.route('/api/check')
def check():
    uid    = request.args.get('uid')
    region = request.args.get('region')
    if not uid:
        return jsonify({'error': 'uid is required'}), 400
    result = check_uid(uid, region)
    code   = 200 if result.get('status') == 'success' else 404
    return jsonify(result), code


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


# Vercel serverless entry point
from flask import Flask
def handler(req, res):
    return app(req, res)
