# Stage 1: Build the Next.js application
FROM node:18-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package files to install dependencies
# Note: The 'frontend/' prefix is necessary because the build context is the project root (../)
COPY frontend/package.json .
COPY frontend/package-lock.json .

# Install dependencies
RUN npm install

# Copy the rest of the frontend source code
# We copy the 'frontend' directory's contents into the WORKDIR /app
COPY frontend .

# Build the Next.js application for production
# CRITICAL FIX IN ENVIRONMENT VARIABLE:
# We explicitly set NEXT_PUBLIC_API_URL to the backend service name (backend)
# on the internal Docker network.
# This variable is needed at build time for next.js to know the API server location.
ENV NEXT_PUBLIC_API_URL=http://backend:8000
RUN npm run build

# Stage 2: Production runtime image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Set the environment variable for the API URL in the final runtime container
ENV NEXT_PUBLIC_API_URL=http://backend:8000

# Copy Next.js configuration, static files, and the built application from the builder stage
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Expose the port the Next.js server runs on
EXPOSE 3000

# Start the Next.js application in production mode
CMD ["npm", "start"]