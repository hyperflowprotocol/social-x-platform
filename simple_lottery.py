#!/usr/bin/env python3
import http.server
import socketserver
import json
import random
from datetime import datetime, timedelta

PORT = 7000

class LotteryHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """<!DOCTYPE html>
<html><head><title>CryptoLotto</title>
<style>
body{font-family:Arial;background:#1a1a2e;color:white;text-align:center;padding:50px}
.prize{font-size:3em;color:#ffd700;margin:20px}
.countdown{font-size:2em;color:#ff6b6b;margin:20px}
input{padding:10px;margin:10px;border:none;border-radius:5px}
button{padding:15px 30px;background:#ffd700;color:#1a1a2e;border:none;border-radius:5px;font-size:1.2em;cursor:pointer}
.winner{background:rgba(255,255,255,0.1);margin:10px;padding:15px;border-radius:5px}
</style></head>
<body>
<h1>🎲 CryptoLotto</h1>
<div class="prize" id="prize">Loading...</div>
<div class="countdown" id="countdown">Loading...</div>
<input type="text" placeholder="Wallet Address" id="wallet">
<input type="number" placeholder="Tickets (0.1 SOL each)" id="tickets" min="1" max="100">
<br><button onclick="buyTickets()">Buy Tickets</button>
<h2>Recent Winners</h2>
<div id="winners">Loading...</div>
<script>
async function loadData(){
  try{
    let res = await fetch('/api/lottery');
    let data = await res.json();
    document.getElementById('prize').innerHTML = data.prize + ' SOL';
    document.getElementById('countdown').innerHTML = 'Next Draw: ' + data.countdown;
    document.getElementById('winners').innerHTML = data.winners.map(w => 
      '<div class="winner">' + w.address.slice(0,8) + '... won ' + w.prize + ' SOL</div>'
    ).join('');
  }catch(e){console.error(e)}
}
function buyTickets(){
  let wallet = document.getElementById('wallet').value;
  let tickets = document.getElementById('tickets').value;
  if(!wallet || !tickets) return alert('Enter wallet and tickets');
  alert('Would buy ' + tickets + ' tickets for ' + (tickets * 0.1) + ' SOL');
}
loadData();
setInterval(loadData, 5000);
</script>
</body></html>"""
            self.wfile.write(html.encode())
        elif self.path == "/api/lottery":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {
                "prize": round(random.uniform(50, 500), 2),
                "countdown": "2h 15m",
                "winners": [
                    {"address": f"ABC{random.randint(10000,99999)}DEF", "prize": round(random.uniform(10, 100), 2)}
                    for _ in range(5)
                ]
            }
            self.wfile.write(json.dumps(data).encode())

print("🎲 CryptoLotto starting on port", PORT)
with socketserver.TCPServer(("0.0.0.0", PORT), LotteryHandler) as httpd:
    httpd.serve_forever()