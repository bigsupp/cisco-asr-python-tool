# cisco-asr-python-tool
Simple Cisco ASR1000 Python Tool

- copy from `config.yml.sample` to `config.yml`
- changes device name, ip, and username as desired, as an example:
```
asr:
  nodebkk1:
    ip: "192.168.1.1"
    username: "bkk1user"
  nodebkk2:
    ip: "192.168.1.2"
    username: "bkk2user"
```
- to run script against `nodebkk1` (from above example), executes `python asr.py nodebkk1`
- executing just `python asr.py nodebkk1`, without arguments, will show available commands.
- executes the script with arguments as needed, that's it.
