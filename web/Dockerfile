FROM node:18-alpine
WORKDIR /app
COPY package.json tsconfig.json vite.config.ts tailwind.config.js postcss.config.js index.html ./
COPY src ./src
RUN npm install
CMD ["npm","run","dev"]
