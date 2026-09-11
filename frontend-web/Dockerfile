# frontend-web/Dockerfile

# Lightweight Node image — React only needs Node to run its dev server
FROM node:20-alpine

WORKDIR /app

# Copy package files first, install, THEN copy the rest of the source.
# This lets Docker cache the npm install layer, so editing your code
# later doesn't force a full reinstall of every dependency.
COPY package*.json ./
RUN npm install

COPY . .

# React's dev server default port
EXPOSE 3000

CMD ["npm", "start"]