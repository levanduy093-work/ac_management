## Environment setup for API token

This project supports loading environment variables from a local `.env` file (using python-dotenv). The `.env` file is ignored by git.

Steps:

1. Create a `.env` file in the project root based on `.env.example`:
   
   API_TOKEN=change_me_to_a_strong_token

2. Start the web server:
   
   - `make run-web` (or `python run_web.py`)

3. Clients must include the token on every request:
   - Header: `X-API-Key: <token>`
   - or Query string: `?api_key=<token>`

Notes:
- WebSocket endpoints also require the same token (header or query param).
- If `API_TOKEN` is not set, the app uses a default token value from the code.

