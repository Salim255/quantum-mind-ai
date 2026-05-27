# =========================
# STAGE 1: BUILD ANGULAR APP
# =========================
FROM node:20-alpine AS build

# Set working directory inside container
WORKDIR /app

# Copy dependency files first (for caching optimization)
COPY package*.json ./

# Install dependencies (clean & CI-safe)
RUN npm install

# Copy full project source code
COPY . .

# Build Angular production bundle
RUN npm run build -- --configuration production


# =========================
# STAGE 2: SERVE WITH NGINX
# =========================
FROM nginx:1.25-alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy Angular build output to nginx folder
COPY --from=build /app/dist/qunatummind-ui/browser /usr/share/nginx/html

# Copy custom nginx config (IMPORTANT for Angular routing)
# This enables SPA fallback (deep linking support)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
