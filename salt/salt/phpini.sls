/etc/php.ini:
  file.managed:
    - source: salt://php.ini
    - user: root
    - group: root
    - mode: 644
