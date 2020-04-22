FROM  postgres:alpine
COPY rates.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
