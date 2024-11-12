
## 数据库初始化
```
echo "初始化数据库"
mysql -u root < docs/sql/create_database.sql

echo "初始化数据表"
mysql formas -u formas -pG097YDcej_6 < docs/sql/create_tables.sql
```

## 备份
```
mysqldump formas -u formas -pG097YDcej_6 > formas.sql
```

## reload
```
mysql formas -u formas -pG097YDcej_6 < formas.sql
```
