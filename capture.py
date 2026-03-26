from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import json

API_KEY = "YOUR_SHOPIFY_API_KEY"
API_SECRET = "YOUR_SHOPIFY_API_SECRET"
SCOPES = "read_products,write_products,read_orders,read_customers,read_analytics,read_marketing_events,write_marketing_events"
REDIRECT_URI = "http://localhost:3000/callback"

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/callback" and "code" in params:
            code = params["code"][0]
            shop = params["shop"][0]
            print(f"\nGot code: {code}")
            print("Exchanging for access token...")

            data = json.dumps({
                "client_id": API_KEY,
                "client_secret": API_SECRET,
                "code": code
            }).encode()

            req = urllib.request.Request(
                f"https://{shop}/admin/oauth/access_token",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req)
            result = json.loads(resp.read())
            token = result.get("access_token")
            print(f"\n✓ ACCESS TOKEN: {token}\n")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Success! Token: {token}".encode())

        else:
            shop = params.get("shop", ["6heu4e-1q.myshopify.com"])[0]
            auth_url = (
                f"https://{shop}/admin/oauth/authorize"
                f"?client_id={API_KEY}&scope={SCOPES}"
                f"&redirect_uri={REDIRECT_URI}&state=nonce123"
            )
            self.send_response(302)
            self.send_header("Location", auth_url)
            self.end_headers()

    def log_message(self, *args):
        pass

print("Listening on http://localhost:3000 ...")
server = HTTPServer(("", 3000), H)
server.handle_request()  # initial redirect
server.handle_request()  # OAuth callback
