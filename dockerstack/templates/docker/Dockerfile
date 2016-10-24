# Start from PHP
# Take a look at the PHP container documentation on the Dockerhub for more detailed
# info on running the container: https://hub.docker.com/_/php/
FROM php:{{image}}
MAINTAINER {{maintainer}}

# Copy PHP config file
COPY conf/php/php.ini /usr/local/etc/php/

# Copy Apache vhost
COPY {{vhost}} /etc/apache2/sites-available/

# Install lib dependencies
RUN apt-get update && \
    apt-get install -y \
		{% for lib in libs %}{{lib}}{% if not loop.last %} \{% endif %}
        {% endfor %}
# Install and configure PHP extensions
RUN docker-php-ext-configure pdo_mysql --with-pdo-mysql=mysqlnd && \
    docker-php-ext-configure mysqli --with-mysqli=mysqlnd && \
    {% for ext in extensions %}docker-php-ext-install {{ext}}{% if not loop.last %} && \{% endif %}
	{% endfor %}
{{extra}}

# Enable site Apache2
RUN a2ensite {{site}}

# Restart Apache
RUN service apache2 restart