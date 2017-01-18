/etc/security/limits.conf:
  file.managed:
    - source: salt://hlimits.conf
    - user: root
    - group: root
    - mode: 644
