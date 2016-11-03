# Start from PHP
# Take a look at the PHP container documentation on the Dockerhub for more detailed
# info on running the container: https://hub.docker.com/_/php/
FROM php:{{image}}
MAINTAINER {{maintainer}}

# Copy PHP config file
COPY conf/php/php.ini /usr/local/etc/php/

# Copy Apache vhost
COPY conf/apache2/sites-available/{{site}} /etc/apache2/sites-available/

# Install lib dependencies
RUN apt-get update && \
    apt-get install -y \
		{% for lib in libs %}{{lib}} {% endfor %}

{% if pecl %}# PECL install extensions
{% for p in pecl %}RUN pecl install {{p}} && docker-php-ext-enable {{p}}{% endfor %}{% endif %}

{% if configure %}# Docker PHP extension configure
RUN {% for ext in configure %}docker-php-ext-configure {{ext}} {% if not loop.last %}&& {% endif %}{% endfor %}{% endif %}

{% if extensions %}# Docker PHP extension install
RUN {% for ext in extensions %}docker-php-ext-install {{ext}} {% if not loop.last %}&& {% endif %}{% endfor %}{% endif %}

{% if enable %}# Docker PHP extension enable
RUN {% for e in enable %}docker-php-ext-enable {{e}} {% if not loop.last %}&& {% endif %}{% endfor %}{% endif %}

{{extra}}

{% if server_engine == 'apache2' %}
# Enable site Apache2
RUN a2ensite {{site}}

{% if modules %}{% for module in modules %}
RUN a2enmod {{module}}
{% endfor %}{% endif %}

# Restart Apache
RUN service apache2 restart
{% endif %}