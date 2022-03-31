#!/bin/bash
sudo -u postgres psql -c "CREATE DATABASE horalibre_db_11479;"
sudo -u postgres psql -c "CREATE USER hl_admin WITH PASSWORD 'h@r$l1br3@119f4';"
sudo -u postgres psql -c "ALTER USER hl_admin WITH PASSWORD 'h@r$l1br3@119f4';
ALTER ROLE hl_admin SET client_encoding TO 'utf8';
ALTER ROLE hl_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE hl_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE horalibre_db_11479 TO hl_admin;"
