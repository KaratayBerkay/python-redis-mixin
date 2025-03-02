FROM redis:7.2-alpine

# Install gettext as root
RUN apk add --no-cache gettext su-exec

# Change ownership of data directories to the redis user
RUN chown -R redis:redis /data
# Change ownership of the redis config directory
RUN mkdir -p /usr/local/etc/redis/etc/redis
RUN chown -R redis:redis /usr/local


# Set the user to run Redis as the non-root user
USER redis

# Start Redis server
CMD ["/bin/sh", "-c", "envsubst < /usr/local/etc/redis/replica.conf.template > /usr/local/etc/redis/replica.conf && redis-server /usr/local/etc/redis/replica.conf"]
