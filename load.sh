cd /home/ubuntu/nginx_page
echo "$(date +"%Y-%m-%d %H:%M:%S") Check if there are changes in the Git repository" >> /var/log/cron.log
if git fetch origin && ! git diff --quiet main..origin/main; then
echo "$(date +"%Y-%m-%d %H:%M:%S") Pulling the latest changes from the Git repository" >> /var/log/cron.log
git pull
else
echo "$(date +"%Y-%m-%d %H:%M:%S") No changes in the Git repository" >> /var/log/cron.log
exit 0
fi

echo "$(date +"%Y-%m-%d %H:%M:%S") Copy nginx.conf to Nginx configuration">> /var/log/cron.log
sudo cp nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
sudo systemctl restart nginx

echo "$(date +"%Y-%m-%d %H:%M:%S") Copy index.html to Nginx document root">> /var/log/cron.log
sudo cp nginx/index.html /var/www/html/
sudo systemctl restart nginx