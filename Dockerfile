FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libmariadb-dev libmariadb-dev-compat gcc && \
    if [ ! -e /usr/local/bin/mariadb_config ] && [ -e /usr/bin/mariadb_config ]; then ln -s /usr/bin/mariadb_config /usr/local/bin/mariadb_config; fi && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography mariadb

COPY app app
COPY migrations migrations
COPY haustierverleih.py config.py boot.sh setup.py ./
RUN chmod a+x boot.sh

ENV FLASK_APP=haustierverleih.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]