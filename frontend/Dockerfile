


# frontend/Dockerfile
FROM nginx:1.25-alpine

# Set working dir (optional)
WORKDIR /usr/share/nginx/html

# Copy all static files from build context (./frontend) into nginx html folder
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
