/etc/telegraf/telegraf.conf:
  file.managed:
    - source: salt://htelegraf.conf
    - user: root
    - group: root
    - mode: 644
