#!/usr/bin/env bash
# This script setes up web servers for the deployment of web_static

# install nginx if it does'nt exist
if ! command -v "nginx" &> /dev/null; then
	sudo apt-get update
	sudo apt-get install -y nginx
fi
# Create folders if don't exist

folder_name1="/data/"
if [ ! -d "$folder_name1" ]; then
	sudo mkdir "$folder_name1"
fi
folder_name2="/data/web_static/"
if [ ! -d "$folder_name2" ]; then
	sudo mkdir "$folder_name2"
fi
folder_name3="/data/web_static/releases/"
if [ ! -d "$folder_name3" ]; then
	sudo mkdir "$folder_name3"
fi
folder_name4="/data/web_static/shared/"
if [ ! -d "$folder_name4" ]; then
	sudo mkdir "$folder_name4"
fi
folder_name5="/data/web_static/releases/test/"
if [ ! -d "$folder_name5" ]; then
	sudo mkdir "$folder_name5"
fi
# Create a simple HTML file to test config
sudo echo "\
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Recreate symbolic link with every execution of this script
symb_link="/data/web_static/current"
if [ -L "$symb_link" ]; then
	sudo rm "$symb_link"
	sudo ln -s /data/web_static/releases/test/ /data/web_static/current
else
	sudo ln -s /data/web_static/releases/test/ /data/web_static/current
fi

# Give ownership of the /data/ folder to the ubuntu user AND group recusively

sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
line="\tlocation /hbnb_static/ {\n      alias /data/web_static/current/;\n     index index.html;\n}"
file="/etc/nginx/sites-available/default"

if ! grep -q "$line" "$file"; then
	sudo sed -i '26 i\ '"$line"'' "$file"
fi
sudo service nginx restart

