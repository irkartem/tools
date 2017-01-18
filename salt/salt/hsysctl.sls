/etc/sysctl.conf:
  file.managed:
    - source: salt://hsysctl.conf
    - user: root
    - group: root
    - mode: 644
