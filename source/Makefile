CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=

.PRECIOUS: %.cdat

LIBCPPFLAGS=-Ofast -I ./src/lib/include -I ./src/lib/graph -I ./src/lib/math -I ./src/lib/third_party -I ./src/lib/utility -I ./src/lib/svm -I ./src/lib/opengl -I ./src/lib -I ./src/include -g
LIBLDFLAG=
LIBLDLIBS=

GEMM=eigen
TARGET=pi2

$(warning GEMM=$(GEMM))
$(warning TARGET=$(TARGET))

LIBSRCS := $(shell find src/lib -name '*.cpp' -not -name '._*')
LIBOBJS := $(subst .cpp,.o,$(LIBSRCS))

ifeq ($(GEMM),eigen)
LIBCPPFLAGS += -I../eigen -DUSE_EIGEN_GEMM=1 
endif

ifeq ($(TARGET),pi2)
LIBCPPFLAGS += \
-mcpu=cortex-a7 \
-mfpu=neon-vfpv4 \
-mfloat-abi=hard
endif

TOOLCPPFLAGS := -O3 -I ./src/include -g

TOOLSRCS := $(shell find src/tool -name '*.cpp' -not -name '._*')
TOOLOBJS := $(subst .cpp,.o,$(TOOLSRCS))

all: jpcnn

%.cdat: %.asm
	m4 -I ./src/lib/pi/ $< | qpu-asm -o $(basename $@).cdat -c g_$(notdir $(basename $@))Code

%.do: %.cdat
	$(CXX) $(CPPFLAGS) -x c -c $< -o $(basename $@).do	

libjpcnn.so: CPPFLAGS=$(LIBCPPFLAGS)
libjpcnn.so: $(LIBOBJS)
	g++ -shared $(LIBLDFLAGS) -o libjpcnn.so $(LIBOBJS) $(LIBLDLIBS) 

main.o: src/tool/main.cpp
	$(CXX) $(CPPFLAGS) -c src/tool/main.cpp -o main.o

jpcnn: CPPFLAGS=$(TOOLCPPFLAGS)
jpcnn: libjpcnn.so $(TOOLOBJS)
	g++ -o jpcnn $(TOOLOBJS) -L. -ljpcnn

%.o: %.cpp
	$(CXX) $(CPPFLAGS) -fPIC -c $< -o $(basename $@).o

clean:
	find . -iname "*.o" -exec rm '{}' ';'
	find . -iname "*.do" -exec rm '{}' ';'
