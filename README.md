nettail
=======

Fetch your router's system log, display it on screen like tail -f and save daily logs when you run this program. Keep track of when your internet connection went down.

Only supports HTTP Basic Authentication for now.

Usage
=====

  cp sample_config.py config.py
  vim config.py  # just edit it to fill in the router URL and HTTP Basic Auth info
  mkdir logs
  python nettail.py
