# Stage 1: Install dependencies and build the project
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package.json .
COPY frontend/package-lock.json .

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY frontend .

# Build the Next.js application
RUN npm run build

# Stage 2: Production runtime image
FROM node:18-alpine

WORKDIR /app

# Set environment variable for Next.js to run in a standalone directory
ENV NEXT_TELEMETRY_DISABLED 1

# Copy files from the builder stage
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Set the API URL for the frontend. 
# 'backend' is the service name in docker-compose.yml
ENV NEXT_PUBLIC_API_URL=http://backend:8000

EXPOSE 3000

# The default command to run the application
CMD ["node", "server.js"]