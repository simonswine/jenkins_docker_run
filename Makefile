# Makefile for creating our standalone Cython program
PYTHON=python
PYVERSION=$(shell $(PYTHON) -c "import sys; print(sys.version[:3])")

INCDIR=$(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_python_inc())")
PLATINCDIR=$(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_python_inc(plat_specific=True))")
LIBDIR1=$(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
LIBDIR2=$(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_config_var('LIBPL'))")
PYLIB=$(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_config_var('LIBRARY')[3:-2])")

CC=$(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('CC'))")
LINKCC=$(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('LINKCC'))")
LINKFORSHARED=$(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('LINKFORSHARED'))")
LIBS=$(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('LIBS'))")
SYSLIBS= $(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('SYSLIBS'))")

SCRIPT_NAME=jenkins_docker_run

INSTALL=install
MKDIR=mkdir -p

DESTDIR=
# Root directory for final installation
PREFIX = /usr

# Location of binaries:
bin_dir = ${PREFIX}/bin/


$(SCRIPT_NAME): $(SCRIPT_NAME).o
	$(LINKCC) -o $@ $^ -L$(LIBDIR1) -L$(LIBDIR2) -l$(PYLIB) $(LIBS) $(SYSLIBS) $(LINKFORSHARED)

$(SCRIPT_NAME).o: $(SCRIPT_NAME).c
	$(CC) -c $^ -I$(INCDIR) -I$(PLATINCDIR)

CYTHON=cython
$(SCRIPT_NAME).c: $(SCRIPT_NAME).py
	$(CYTHON) --embed $(SCRIPT_NAME).py

all: $(SCRIPT_NAME)

install: $(SCRIPT_NAME)
	$(MKDIR) $(DESTDIR)$(bin_dir)
	$(INSTALL) -m755 $(SCRIPT_NAME) $(DESTDIR)$(bin_dir)

clean:
	@echo Cleaning $(SCRIPT_NAME)
	@rm -f *~ *.o *.so core core.* *.c $(SCRIPT_NAME)
