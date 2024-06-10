FROM node:latest

WORKDIR /code
ADD ./web /code
# ADD ./web/package.json /code/package.json
# ADD ./web/package-lock.json /code/package-lock.json
# ADD ./web/index.html /code/index.html
# ADD ./web/src /code/src
# ADD ./web/public /code/public

RUN npm install

# move the installed node_modules to / so that the build command (in disco.json)
# will see it when running npm run build
# Cannot `mv /code /`
RUN mv /code/node_modules /node_modules
RUN mv /code/package.json /
RUN mv /code/index.html /
RUN mv /code/src /src
RUN mv /code/public /public
