# Frontend Dockerfile for Next.js production
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile

# Copy all source code
COPY . .

# Build Next.js app
RUN npm run build

# Expose port
EXPOSE 3000

# Start Next.js app
CMD ["npm", "run", "start"]
