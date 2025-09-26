FROM node:18-alpine AS builder
WORKDIR /app
COPY frontend/package.json .
COPY frontend/package-lock.json .
RUN npm install
COPY frontend .
ENV NEXT_PUBLIC_API_URL=http://backend:8000
RUN npm run build

# Stage 2: Production runtime image
FROM node:18-alpine
WORKDIR /app
ENV NEXT_PUBLIC_API_URL=http://backend:8000
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "start"]