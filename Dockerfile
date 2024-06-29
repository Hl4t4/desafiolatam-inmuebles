FROM python:3.12.4-alpine3.20

# ENV

ARG SECRET_KEY=DEFAULT_WRONG
ARG EMAIL_BACKEND=DEFAULT_WRONG
ARG EMAIL_HOST=DEFAULT_WRONG
ARG EMAIL_PORT=DEFAULT_WRONG
ARG EMAIL_USE_TLS=DEFAULT_WRONG
ARG EMAIL_HOST_USER=DEFAULT_WRONG
ARG EMAIL_HOST_PASSWORD=DEFAULT_WRONG
ARG DEFAULT_FROM_EMAIL=DEFAULT_WRONG
ARG DEFAULT_CONTACT_NOTICE_EMAIL=DEFAULT_WRONG
ARG ARG BDD_NAME=DEFAULT_WRONG
ARG BDD_USER=DEFAULT_WRONG
ARG BDD_PASSWORD=DEFAULT_WRONG
ARG BDD_HOST=DEFAULT_WRONG
ARG BDD_PORT=DEFAULT_WRONG

ENV SECRET_KEY=${SECRET_KEY}
ENV EMAIL_BACKEND=${EMAIL_BACKEND}
ENV EMAIL_HOST=${EMAIL_HOST}
ENV EMAIL_PORT=${EMAIL_PORT}
ENV EMAIL_USE_TLS=${EMAIL_USE_TLS}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
ENV DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}
ENV DEFAULT_CONTACT_NOTICE_EMAIL=${DEFAULT_CONTACT_NOTICE_EMAIL}
ENV BDD_NAME=${BDD_NAME}
ENV BDD_USER=${BDD_USER}
ENV BDD_PASSWORD=${BDD_PASSWORD}
ENV BDD_HOST=${BDD_HOST}
ENV BDD_PORT=${BDD_PORT}

# Set working directory


WORKDIR /usr/inmuebles
# RUN mkdir -p /usr/inmuebles/static

# New User
RUN adduser -D hlata
# RUN adduser hlata sudo
# RUN grep sudo /etc/group

#RUN adduser -D $USER && mkdir -p /etc/sudoers.d \
        #&& echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
        #&& chmod 0440 /etc/sudoers.d/$USER

# Copy data
COPY ./requirements.txt ./
COPY ./startcmd.sh ./
COPY ./inmuebles/ ./

# Update Linux and install dependencies
RUN apk update && apk upgrade && apk add --no-cache make g++ openssh libpq-dev postgresql-dev postgresql postgresql-contrib bind-tools curl

# Install pip packages
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

# Load Postgresql data
# RUN python manage.py migrate
# RUN python manage.py loaddata web/fixtures/regiones.json
# RUN python manage.py loaddata web/fixtures/comunas.json
# RUN python manage.py loaddata web/fixtures/tipos_usuarios.json
# RUN python manage.py loaddata web/fixtures/tipos_inmuebles.json
# RUN python manage.py loaddata web/fixtures/usuarios.json
# RUN python manage.py loaddata web/fixtures/inmuebles.json 
# RUN python manage.py loaddata web/fixtures/solicitudes_arriendo.json

# Load Statics
# RUN python manage.py collectstatic --noinput

# Expose the listening port
EXPOSE 80

# Change user
USER hlata

# Launch app
# RUN gunicorn inmuebles.wsgi --bind=0.0.0.0:80 
CMD sh /usr/inmuebles/startcmd.sh
