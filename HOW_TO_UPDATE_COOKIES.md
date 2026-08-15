# How to Update Cookies When API Stops Working

The datadome cookie expires every few weeks. Here's how to get fresh ones:

## Steps (Mobile Chrome)

1. Open Chrome → go to https://shop2game.com/app/100067/idlogin
2. Wait for page to fully load
3. Tap address bar → type: javascript:document.cookie
4. Press Enter
5. You'll see all cookies — copy the values of:
   - datadome=xxxxx
   - session_key=xxxxx
6. Open api/index.py → update COOKIES section with new values
7. Commit to GitHub → Vercel auto-redeploys

## Steps (PC Chrome)

1. Go to https://shop2game.com/app/100067/idlogin
2. Press F12 → Application tab → Cookies → shop2game.com
3. Copy datadome and session_key values
4. Update api/index.py COOKIES section
5. Commit → redeploy
