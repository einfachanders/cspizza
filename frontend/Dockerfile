# --- Build Stage ---
FROM node:lts-bookworm AS builder

WORKDIR /app/frontend

# Copy package.json and package-lock.json first for caching npm install
COPY package.json package-lock.json ./
# Use 'ci' for reproducibility, omit dev dependencies for production
RUN npm install

# Copy necessary files (source, environment, vite)
COPY src ./src
COPY public ./public
COPY .env.production ./.env 
COPY index.html ./index.html
COPY vite.config.js ./vite.config.js

RUN npm run build

# --- Nginx Runtime Stage ---
ARG spark_version
FROM nginx:latest AS runtime
WORKDIR /usr/share/nginx/html

# Remove default nginx configs
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy built frontend files
COPY --from=builder /app/frontend/dist ./

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set proper permissions
RUN chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html

RUN chown -R nginx:nginx /var/cache/nginx
# Replace the nginx pid file with a temporary one
# where the nginx user has access to
RUN sed -i 's,/var/run/nginx.pid,/tmp/nginx.pid,' /etc/nginx/nginx.conf

USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
