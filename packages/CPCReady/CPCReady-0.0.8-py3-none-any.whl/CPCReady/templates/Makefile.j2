PROJECT_CFG = cfg/project.cfg
EMULATORS_CFG = cfg/emulators.cfg
EMULATOR = rvm-web

all: build run

.PHONY: read-project-config
read-project-config:
	@if [ -f $(PROJECT_CFG) ]; then \
		MODEL=$$(awk -F'=' '/model/{print $$2}' $(PROJECT_CFG)); \
		NAME=$$(awk -F'=' '/name/{print $$2}' $(PROJECT_CFG)); \
    else \
		echo "El archivo $(PROJECT_CFG) no existe."; \
		exit 1; \
    fi

.PHONY: build
build: read-project-config
	@cpcr_build --build

.PHONY: check-emulators-config
check-emulators-config:
	@if [ ! -f $(EMULATORS_CFG) ]; then \
		echo "El archivo $(EMULATORS_CFG) no existe."; \
        exit 1; \
 	fi

.PHONY: run
run: check-emulators-config
	@cpcr_run --emulator $(EMULATOR)