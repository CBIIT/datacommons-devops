# Build stage
ARG ECR_REPO
FROM maven:3.8.5-openjdk-17 as build
WORKDIR /usr/src/app
COPY . .
RUN mvn package -DskipTests

# Production stage
FROM ${ECR_REPO}/base-images:backend-jdk17
RUN rm -rf /usr/local/tomcat/webapps/ROOT
COPY --from=build /usr/src/app/target/Bento-0.0.1.war /usr/local/tomcat/webapps/ROOT.war
