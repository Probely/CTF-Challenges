FROM openjdk:8-jre-slim

RUN addgroup --system p100 && \
	adduser --system --home /p100 --disabled-login --shell /bin/false p100 && \
	adduser --system --home /var/empty --disabled-login --shell /bin/false --gecos "flag{Rw4btOtmNCytflW9uFMN}" flag && \
	apt-get update -y && \
	apt-get install wget curl netcat-traditional -y

COPY ./target/dependency /p100/lib
COPY ./target/highway-trouble.jar /p100
WORKDIR /p100

EXPOSE 32100

USER p100
CMD ["java", "-jar", "highway-trouble.jar", "--listen=8080"]
