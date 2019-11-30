FROM node:10.15-alpine

# Update OS
RUN apk --no-cache add ca-certificates && update-ca-certificates

# Install npm package in a layer to cache as these rarely change
WORKDIR /opt/app
COPY ./package.json ./yarn.lock ./
RUN yarn install --no-cache --production

COPY . /opt/app

CMD ["yarn", "migrate"]