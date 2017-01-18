/root/.ssh/authorized_keys:
  file.managed:
    - source: salt://authorized_keys
    - user: root
    - group: root
    - mode: 644
