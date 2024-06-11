FROM node:latest

WORKDIR /code
COPY ./web/package.json /code/package.json
COPY ./web/package-lock.json /code/package-lock.json
RUN npm install

# move the installed node_modules to / so that the build command (in disco.json)
# will see it when running npm run build
# Cannot `mv /code /`
COPY ./web /code/.
RUN npm run build
