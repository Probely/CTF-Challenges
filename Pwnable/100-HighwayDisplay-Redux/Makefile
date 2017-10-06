
all: target 

target:
	mvn dependency:copy-dependencies package

docker: guard-SERVICE_NAME target 
	sudo docker build -t ${SERVICE_NAME} .

clean:
	mvn clean

distclean: clean

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install: guard-SERVICE_NAME docker
	sudo ln -sf "$(shell echo $$PWD)/${SERVICE_NAME}.service" /etc/systemd/system/${SERVICE_NAME}.service
	sudo systemctl daemon-reload

uninstall: guard-SERVICE_NAME
	sudo systemctl stop ${SERVICE_NAME} >/dev/null 2>&1 || true
	sudo rm -f /etc/systemd/system/${SERVICE_NAME}.service
	sudo systemctl daemon-reload
	sudo docker rmi ${SERVICE_NAME}

.PHONY: all clean distclean install uninstall tests
