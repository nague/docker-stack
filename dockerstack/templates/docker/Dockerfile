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
		{% for lib in libs %}{{lib}} {% endfor %}

# Install and configure PHP extensions
{% if configure %}RUN {% for ext in configure %}{{ext}} {% if not loop.last %}&& {% endif %}{% endfor %}{% endif %}
{% if extensions %}RUN {% for ext in extensions %}docker-php-ext-install {{ext}} {% if not loop.last %}&& {% endif %}{% endfor %}{% endif %}

{{extra}}

# Enable site Apache2
RUN a2ensite {{site}}

# Restart Apache
RUN service apache2 restart