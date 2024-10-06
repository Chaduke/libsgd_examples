# this is just a simple makefile to get started 
# will add fancy features as I get more educated on the subject

build:	
	gcc -Iinclude -Llib -DSGD_DYNAMIC=1 -o ex001.exe ex001.c -lsgd_dynamic
	gcc -Iinclude -Llib -DSGD_DYNAMIC=1 -o ex002.exe ex002.c -lsgd_dynamic
	gcc -Iinclude -Llib -DSGD_DYNAMIC=1 -o ex003.exe ex003.c -lsgd_dynamic
	gcc -Iinclude -Llib -DSGD_DYNAMIC=1 -o ex004.exe ex004.c -lsgd_dynamic

run:
	./ex001.exe

clean:
	rm *.exe
	rm *.obj