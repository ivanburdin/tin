#!/bin/bash

pip install /tmp/colorama-0.3.9-py2.py3-none-any.whl
pip install /tmp/netaddr-0.7.19-py2.py3-none-any.whl
pip install /tmp/psutil-5.4.7.tar.gz
pip install /tmp/yara-python-3.8.1.tar.gz
pip install /tmp/pylzma-0.4.9.tar.gz

cd /tmp && tar -xf /tmp/loki.tar
cd /tmp/Loki && python /tmp/Loki/loki.py -l /tmp/Loki/out.log --dontwait -p / && pwd