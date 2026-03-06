FROM eclipse-temurin:17-jdk

WORKDIR /app
COPY . /app
RUN chmod +x /app/build_server.sh /app/run_server.sh

CMD ["bash", "-lc", "./run_server.sh"]
