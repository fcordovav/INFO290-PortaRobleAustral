ARG NODE_VERSION=20.17.0

FROM node:${NODE_VERSION}-alpine

WORKDIR /app

COPY package.json package-lock.json /app/

RUN npm install

COPY . /app

EXPOSE 3008

CMD npm run build && npm install -g serve && serve -s build -l 3008