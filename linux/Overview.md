# Linux Command cheatsheet

## Table of Contents
- [Linux Command cheatsheet](#linux-command-cheatsheet)
  - [Table of Contents](#table-of-contents)
  - [Authorization](#authorization)
  - [Storage](#storage)
    - [Hard disk listing](#hard-disk-listing)
    - [Files/Folders sizes](#filesfolders-sizes)
  - [Docker](#docker)
    - [Save / Load Docker images](#save--load-docker-images)
    - [Docker volumes prune](#docker-volumes-prune)
  - [PostgreSQL](#postgresql)
    - [Usage with Docker](#usage-with-docker)
  - [Save backup file](#save-backup-file)
  - [Restore to DB](#restore-to-db)


## Authorization

Change ownership of folders/files
```bash
chown -R ${USER} ${PATH}
```

## Storage

### Hard disk listing
How many hard-disk are avaiable and how much were comsumed
```bash
df -h
```

### Files/Folders sizes
List files/folders in path toghether with their size, sort reversed
```bash
sudo du -h -d 1 ${PATH} | sort -rh
```

## Docker

### Save / Load Docker images
```bash
docker save ${IMAGE_NAME} > ${IMAGE_FILE_NAME}.tar
docker load < ${IMAGE_FILE_NAME}.tar
```

### Docker volumes prune
```bash
docker volume prune
```

## PostgreSQL

### Usage with Docker

## Save backup file
```bash
docker exec ${PSQL_CONTAINER_NAME} pg_dump -U ${PSQL_USER_NAME} -d ${PSQL_DB_NAME} > ${BACKUP_NAME}.sql
```

## Restore to DB
```bash
docker exec -i ${PSQL_CONTAINER_NAME} psql -U ${PSQL_USER_NAME} -d ${PSQL_DB_NAME} < ${BACKUP_NAME}.sql
```
