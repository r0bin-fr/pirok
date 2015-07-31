obj-m += flow.o
flow-objs := flow-main.o

all:
	make ARCH=arm CROSS_COMPILE=${CCPREFIX} -C ../../kernel/linux M=$(PWD) modules

clean:
	make ARCH=arm CROSS_COMPILE=${CCPREFIX} -C ../../kernel/linux M=$(PWD) clean
