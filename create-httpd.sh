mkdir /home/ec2-user/http-data
chmod 777 /home/ec-user/http-data
docker run -dit --name httpd -p 80:80 -v /home/ec2-user/http-data:/usr/local/apache2/htdocs httpd:2.4
