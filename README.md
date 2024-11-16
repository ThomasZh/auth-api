# auth-api

auth api for formas service

## 安装依赖包

```
yum install python3
python3 -V
3.9
pip3 install -r requirements.txt
```

## 修改配置文件(for local)

```
cp -rf docs/etc/formas/auth-api.cfg /opt/formas/conf
```

## 创建日志目录

```
mkdir -p /var/log/formas
chmod 777 /var/log/formas
```

or update `path` property in `[log]` section from local `auth-api.cfg`:

```
[log]
path = ~/web/formas-service/log
```

## Init Mysql Database

* Step-1:  Login local mysql server with root user:

> mysql -h 127.0.0.1 -P 3306 -u root -p

* Step-2: Execute `create_database.sql` in mysql console:

> source docs/sql/create_database.sql;

* Step-3: Check newly created database `formas` and user `formas`:

> show databases;
> SELECT user FROM mysql.user;

* Step-4: Execute `create_tables.sq` in mysql console:

> use formas;
> source docs/sql/create_tables.sql;

* Step-5: Exit mysql consle:

> exit

## 运行(Local development)

```
python3 auth_api.py
```

## Start local dev server with config path (Mac OSX)

```
export FORMAS_AUTH_CFG_PATH="~/web/formas-service/auth-api.cfg"
python3 auth_api.py
```

## 项目组
* auth-api

## 目录结构

```
/auth-api
├── docs
├── foo
├── static
├── templates
```

## 部署目录

```
/opt/formas/service/auth-api
```

## Service Deployment

```
cp -rf docs/etc/formas/nginx/conf.d/formas.conf /opt/formas/conf/nginx/conf.d
cp -rf docs/etc/systemd/system/auth-api.service /etc/systemd/system
systemctl restart auth-api.service
systemctl status auth-api.service
systemctl enable auth-api.service
```