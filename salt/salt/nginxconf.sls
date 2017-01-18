/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx.conf
    - user: root
    - group: root
    - mode: 644
