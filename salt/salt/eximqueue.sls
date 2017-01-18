/root/monisp/eximqueue.sh:
  file.managed:
    - source: salt://eximqueue.sh
    - user: root
    - group: root
    - mode: 744
