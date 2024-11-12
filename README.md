# auth-api
auth api for formas service

## 安装依赖包
```
yum install python3
python3 -V
3.9
pip3 install -r requirements.txt
```

## 修改配置文件
```
cp -rf docs/etc/formas/auth-api.cfg /opt/formas/conf
cp -rf docs/etc/formas/nginx/conf.d/formas.conf /opt/formas/conf/nginx/conf.d

cp -rf docs/etc/systemd/system/auth-api.service /etc/systemd/system
systemctl restart auth-api.service
systemctl status auth-api.service
systemctl enable auth-api.service
```

## 创建日志目录
```
mkdir -p /var/log/formas
chmod 777 /var/log/formas
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
