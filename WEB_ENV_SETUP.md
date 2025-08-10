## Environment setup for API token

This project supports loading environment variables from a local `.env` file (using python-dotenv). The `.env` file is ignored by git.

Steps:

1. Create a `.env` file in the project root based on `.env.example`:
   
   API_TOKEN=change_me_to_a_strong_token

2. Start the web server:
   
   - `make run-web` (or `python run_web.py`)

3. New auth model (production-ready):
   - Visit `/login` and enter your password (the value of `API_TOKEN`).
   - The server sets a secure session cookie; all API calls use this session (no token in URLs or JS).

Notes:
- Docs (`/docs`) can be disabled in production via `DISABLE_DOCS=true`.
- Cookies are HTTP-only; for Internet deployment behind HTTPS, set `COOKIE_SECURE=true`.
- State-changing APIs require header `X-Requested-With: XMLHttpRequest` to mitigate CSRF.

