FROM node:12

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . .

RUN npm install

RUN npm run build

EXPOSE 5000

CMD [ "node", "dist/index.js" ]