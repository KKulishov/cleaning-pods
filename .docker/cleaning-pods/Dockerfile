FROM python:3-buster

#https://github.com/kubernetes-client/python

RUN ln -snf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo Europe/Moscow > /etc/timezone

ENV HTTPS_PROXY http://proxy-server.sovcombank.group:3128
ENV HTTP_PROXY http://proxy-server.sovcombank.group:3128
ENV https_proxy http://proxy-server.sovcombank.group:3128
ENV http_proxy http://proxy-server.sovcombank.group:3128
ENV NO_PROXY "127.0.0.1,localhost,.sovcombank.group,minio,.sovcombank.ru,kubernetes,.default.svc.cluster.local"

RUN groupadd -g 1000 python
RUN useradd -s /bin/bash -g python -u 1000 -g 1000 python

RUN mkdir -p /app/lib && chown -R python:python /app
WORKDIR /app/lib

COPY --chown=1000:1000 .docker/cleaning-pods/requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/lib

COPY --chown=1000:1000 .docker/cleaning-pods/entrypoint.sh /app/lib/entrypoint.sh
COPY --chown=1000:1000 .docker/cleaning-pods/main.py /app/lib/

CMD ["/usr/local/bin/python", "/app/lib/main.py"]

USER python

