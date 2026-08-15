# FF UID Checker API — Vercel

Free Fire UID checker using shop2game.com. No guest accounts needed!

## Deploy on Vercel

1. Upload this folder to GitHub
2. Go to vercel.com → New Project → Import repo
3. Framework Preset: **Other**
4. Deploy → Done!

## Endpoints

GET /?uid=2579249340
GET /?uid=2579249340&region=BD
GET /api/check?uid=2579249340&region=BD
GET /api/health

## Response
```json
{
  "status": "success",
  "uid": "2579249340",
  "nickname": "PlayerName",
  "level": 72,
  "region_code": "BD",
  "region_name": "Bangladesh"
}
```

## Supported Regions
BD, IND, SG, MY, ID, PK, ME, BR, TH, VN, TW, RU, CIS, US

## No Spin Down!
Vercel serverless — always on, no cold start issues, completely free!
