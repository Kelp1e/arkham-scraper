FROM node:20-alpine3.17

LABEL version="1.0"
LABEL description="React Frontend for the Real Estate API"

WORKDIR /app

COPY ./package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "start"]

