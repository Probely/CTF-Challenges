all: ransom.tar pwtest

ransom.tar: password
	mkdir -p ransom
	for i in `seq 1 3`; do fortune startrek > ransom/document$${i}.txt; done

	$(eval ANSWER := $(shell dd if=/dev/urandom bs=1024 count=1024 status=none | sha256sum | cut -d' ' -f1))
	echo "This is the answer to this challenge: $(ANSWER)" > ransom/document4.txt

	echo "Password seed is $(shell date +%s)"
	$(eval PASSWORD := $(shell ./password))
	ccrypt -f -K '$(PASSWORD)' -r ransom/document1.txt

	sleep 3  # other files should have a different ctime
	ccrypt -f -K '$(PASSWORD)' -r ransom/document*.txt

	cp password.c ransom/
	tar cf ransom.tar ransom/
	rm -rf ransom/

password: password.c
	gcc -o password password.c

pwtest: pwtest.c
	gcc -o pwtest pwtest.c

clean:
	rm -rf password pwtest ransom.tar ransom/

.PHONY: clean
