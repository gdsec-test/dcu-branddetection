REPONAME=digital-crimes/branddetection
BUILDROOT=$(HOME)/dockerbuild/$(REPONAME)
DOCKERREPO=gdartifactory1.jfrog.io/docker-dcu-local/brand_detection
DATE=$(shell date)
COMMIT=
BUILD_BRANCH=origin/main

define deploy_k8s
	docker push $(DOCKERREPO):$(2)
	cd k8s/$(1) && kustomize edit set image $$(docker inspect --format='{{index .RepoDigests 0}}' $(DOCKERREPO):$(2))
	kubectl --context $(3) apply -k k8s/$(1)
	cd k8s/$(1) && kustomize edit set image $(DOCKERREPO):$(1)
endef

all: init

init:
	pip install -r test_requirements.txt
	pip install -r requirements.txt

.PHONY: lint
lint:
	isort --atomic .
	flake8 --config ./.flake8 .

.PHONY: unit-test
unit-test:
	@echo "----- Running tests -----"
	python -m unittest discover tests "*_tests.py"

.PHONY: testcov
testcov:
	@echo "----- Running tests with coverage -----"
	@coverage run --source=branddetection -m unittest discover tests "*_tests.py"
	@coverage xml
	@coverage report


.PHONY: prep
prep: lint unit-test
	@echo "----- preparing $(REPONAME) build -----"
	mkdir -p $(BUILDROOT)
	cp -rp ./* $(BUILDROOT)
	cp -rp ~/.pip $(BUILDROOT)/pip_config

dev: prep
	@echo "----- building $(REPONAME) dev -----"
	docker build -t $(DOCKERREPO):dev $(BUILDROOT)

test-env: prep
	@echo "----- building $(REPONAME) test -----"
	docker build -t $(DOCKERREPO):test $(BUILDROOT)

ote: prep
	@echo "----- building $(REPONAME) ote -----"
	docker build -t $(DOCKERREPO):ote $(BUILDROOT)

prod: prep
	@echo "----- building $(REPONAME) prod -----"
	read -p "About to build production. Are you sure? (Y/N): " response ; \
	if [[ $$response == 'N' || $$response == 'n' ]] ; then exit 1 ; fi
	if [[ `git status --porcelain | wc -l` -gt 0 ]] ; then echo "You must stash your changes before proceeding" ; exit 1 ; fi
	$(eval COMMIT:=$(shell git rev-parse --short HEAD))
	docker build -t $(DOCKERREPO):$(COMMIT) $(BUILDROOT)

.PHONY: dev-deploy
dev-deploy: dev
	@echo "----- deploying $(REPONAME) dev -----"
	$(call deploy_k8s,dev,dev,dev-cset)

.PHONY: test-deploy
test-deploy: test-env
	@echo "----- deploying $(REPONAME) test -----"
	$(call deploy_k8s,test,test,test-cset)

.PHONY: ote-deploy
ote-deploy: ote
	@echo "----- deploying $(REPONAME) ote -----"
	$(call deploy_k8s,ote,ote,ote-cset)

.PHONY: prod-deploy
prod-deploy: prod
	@echo "----- deploying $(REPONAME) prod -----"
	$(call deploy_k8s,prod,$(COMMIT),prod-cset)

.PHONY: clean
clean:
	@echo "----- cleaning $(REPONAME) app -----"
	rm -rf $(BUILDROOT)
