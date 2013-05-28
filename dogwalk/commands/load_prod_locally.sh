heroku pgbackups:capture
curl -o latest.dump `heroku pgbackups:url`
dropdb dogwalk
createdb dogwalk
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d dogwalk latest.dump

