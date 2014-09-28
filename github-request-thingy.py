import argparse
import hashlib
import hmac
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import pprint
import os
import sys
import subprocess
import getpass
 
HOOK_SECRET_KEY = getpass.getpass()
 
class GithubHookHandler(BaseHTTPRequestHandler):
    def _validate_signature(self, data):
        sha_name, signature = self.headers['X-Hub-Signature'].split('=')
        if sha_name != 'sha1':
            return False
 
        # HMAC requires its key to be bytes, but data is strings.
        mac = hmac.new(HOOK_SECRET_KEY.encode(), msg=data, digestmod=hashlib.sha1)
        return hmac.compare_digest(mac.hexdigest(), signature)
 
    def do_POST(self):
        data_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(data_length)
 
        if not self._validate_signature(post_data):
            self.send_response(401)
            return
 
        payload = json.loads(post_data.decode('utf-8'))
        self.handle_payload(payload)
        self.send_response(200)
        subprocess.call(['sh', 'deploy_git.sh'])
        payload = {'state': 'success'}
        deploy_id = payload["id"]
        r = requests.post("https://api.github.com/repos/Charcoal-SE/SmokeDetector/deployments/:id/statuses", data=payload, headers={'Accept': 'application/vnd.github.cannonball-preview+json'})
 
class MyHandler(GithubHookHandler):
    def handle_payload(self, json_payload):
        """Simple handler that pretty-prints the payload."""
        print('JSON payload')
        pprint.pprint(json_payload)
 
if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    server.serve_forever()
