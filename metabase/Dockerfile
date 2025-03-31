FROM postgres:latest

ENV POSTGRES_USER=metabase
ENV POSTGRES_PASSWORD=metabase
ENV POSTGRES_DB=metabase

RUN mkdir -p /docker-entrypoint-initdb.d

COPY dump_metabase.backup /docker-entrypoint-initdb.d/dump.backup

COPY restore.sh /docker-entrypoint-initdb.d/restore.sh
RUN chmod +x /docker-entrypoint-initdb.d/restore.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]