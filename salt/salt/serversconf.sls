/etc/httpd/conf.d/status.conf:
  file.managed:
    - source: salt://status.conf
    - user: root
    - group: root
    - mode: 644
