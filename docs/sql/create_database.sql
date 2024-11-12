create database formas charset utf8mb4;
create user formas@'%' identified by 'G097YDcej_6';
grant all privileges on `formas`.* to formas@'%';
flush privileges;
create user formas@'localhost' identified by 'G097YDcej_6';
grant all privileges on `formas`.* to formas@'localhost';
flush privileges;

exit
