# ❌ THIS DOCKERFILE IS INTENTIONALLY BROKEN!
# Can you spot and fix the 4 mistakes?

FROM node:22-alpine

# Bug 1: Missing WORKDIR! All files will be placed into root "/"

# Bug 2: Trying to install dependencies before package.json is copied!
RUN npm install

# Copying files
COPY package.json .
COPY server.js .

# Bug 3: Exposing the wrong port! (Code listens on 3000)
EXPOSE 8080

# Bug 4: CMD syntax issue / exec form recommended
CMD node server.js