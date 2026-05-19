# Static site served by nginx. No build step required for the base setup.
# Heavier simulators that need a build (Vite, etc.) can be added later as a
# multi-stage build that drops their `dist/` into the same image.
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy everything but the Docker / repo plumbing (see .dockerignore).
COPY . /usr/share/nginx/html
RUN rm -f /usr/share/nginx/html/Dockerfile \
          /usr/share/nginx/html/nginx.conf \
          /usr/share/nginx/html/deploy.sh \
          /usr/share/nginx/html/docker-compose*.yml \
    && rm -rf /usr/share/nginx/html/.claude

EXPOSE 80
