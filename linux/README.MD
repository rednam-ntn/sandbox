# Linux Command cheatsheet

## Table of Contents
- [Linux Command cheatsheet](#linux-command-cheatsheet)
  - [Table of Contents](#table-of-contents)
  - [Authorization](#authorization)
  - [Storage](#storage)
    - [Hard disk listing](#hard-disk-listing)
    - [Files/Folders sizes](#filesfolders-sizes)
    - [Format Hard Drive file system](#format-hard-drive-file-system)
    - [Mount Hard drive](#mount-hard-drive)
  - [Hardware Information](#hardware-information)
    - [Hard drive list](#hard-drive-list)
    - [CPU](#cpu)
    - [Hardware List](#hardware-list)
  - [Docker](#docker)
    - [Save / Load Docker images](#save--load-docker-images)
    - [Docker volumes prune](#docker-volumes-prune)
  - [PostgreSQL](#postgresql)
  - [Save backup file](#save-backup-file)
    - [Without Docker](#without-docker)
    - [With Docker](#with-docker)
  - [Restore to DB](#restore-to-db)
    - [Without Docker](#without-docker-1)
    - [With Docker](#with-docker-1)
  - [Transfering](#transfering)
  - [SSH](#ssh)
    - [Generate SSH key](#generate-ssh-key)
    - [Copy SSH key to server](#copy-ssh-key-to-server)


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

### Format Hard Drive file system
Should use `fdisk` first to know ${DEVICE_PATH}
```bash
sudo mkfs -t ext4 ${DEVICE_PATH}
```
### Mount Hard drive
```
sudo mount ${DEVICE_PATH} ${ABSOLUTE_PATH}
```

## Hardware Information

### Hard drive list
```bash
sudo fdisk -l
```

### CPU
```bash
lscpu
```

### Hardware List
```bash
lshw
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

## Save backup file
### Without Docker
```bash
pg_dump -h ${PSQL_HOST} -p ${PSQL_PORT} -U ${PSQL_USER_NAME} -d ${PSQL_DB_NAME} > ${BACKUP_NAME}.sql
```

### With Docker
```bash
docker exec ${PSQL_CONTAINER_NAME} pg_dump -U ${PSQL_USER_NAME} -d ${PSQL_DB_NAME} > ${BACKUP_NAME}.sql
```

## Restore to DB
### Without Docker
```bash
psql -h ${PSQL_HOST} -p ${PSQL_PORT} -U ${PSQL_USER_NAME} -d ${PSQL_DB_NAME} < ${BACKUP_NAME}.sql
```
### With Docker
```bash
docker exec -i ${PSQL_CONTAINER_NAME} psql -U ${PSQL_USER_NAME} -d ${PSQL_DB_NAME} < ${BACKUP_NAME}.sql
```


## Transfering
```bash
rsync -ravzh ${SOURCE_PATH} ${DESTINATION_PATH}
```

## SSH
### Generate SSH key
```bash
ssh-keygen -t rsa -b 4096 -C "${USER_EMAIL}"
```

### Copy SSH key to server
```bash
ssh-copy-id -i ${PUBLIC_KEY_PATH}.pub ${SERVER_USER}@${SERVER_IP}
```
or you can copy the public key content directly to the server into file
```
cat ~/.ssh/authorized_keys
```
****