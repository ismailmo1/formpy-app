FROM alpine:latest

# install nginx
# create links to push error and output to log files - var/log/nginx is persistent volume
# remove files to reduce image size
RUN apk --update add nginx && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    mkdir /etc/nginx/sites-enabled/ && \
    mkdir -p /run/nginx && \
    rm -rf /etc/nginx/conf.d/default.conf && \
    rm -rf /var/cache/apk/*

COPY conf.d/app.conf /etc/nginx/conf.d/app.conf

EXPOSE 80 443

CMD ["nginx", "-c", "/etc/nginx/conf.d/app.conf", "-g", "daemon off;"]