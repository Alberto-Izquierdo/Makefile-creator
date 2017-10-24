#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

class MyApp:
    def run(self):
        if len(sys.argv) < 3:
            print ('Usage: ./makefile_generator.py <directory> <Executable name>')
            return
        directory = sys.argv[1]
        path = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(path, directory, 'src')
        if not os.path.isdir(src):
            print ('That folder doesnt contain a src folder')
            return
        CXXFLAGS = ''
        LDFLAGS = ''
        LDLIBS = ''
        with open ('flags.txt', 'r') as flags_file:
            content = flags_file.readlines()
            for line in content:
                if line.startswith('CXXFLAGS:'):
                    CXXFLAGS = line.split(':')[1]
                elif line.startswith('LDFLAGS:'):
                    LDFLAGS = line.split(':')[1]
                elif line.startswith('LDLIBS:'):
                    LDLIBS = line.split(':')[1]
        if (CXXFLAGS == '' or LDFLAGS == '' or LDLIBS == ''):
            print ('Missing data in Flags.txt')
            return
        list_src = []
        for folder in os.listdir(src):
            if os.path.isdir(os.path.join(src, folder)):
                list_src.append(folder)
        string = 'EXEC := ' + sys.argv[2] + '\n\nDIRSRC := src/\n\
DIROBJ := obj/\n'
        for folder in list_src:
            string += 'DIRSRC' + folder.upper() + ':= $(DIRSRC)' + folder + '/\n'
        string += '\nCXX := g++\n\n\
# Compilation flags --------------------------------------------------\n\
CXXFLAGS := -I $(DIRSRC)'
        for folder in list_src:
            string += ' -I $(DIRSRC' + folder.upper() + ')'
        string += CXXFLAGS + '\n\n\
# Linker flags -------------------------------------------------------\n\
LDFLAGS :='  + LDFLAGS + '\n\
LDLIBS :=' + LDLIBS + '\n\n\
# Compilation mode (-mode=release -mode=debug) -----------------------\n\
ifeq ($(mode), release)\n\
\tCXXFLAGS += -O2 -D_RELEASE\n\
else\n\
\tCXXFLAGS += -g -D_DEBUG\n\
\tmode := debug\n\
endif\n\n\
OBJS := $(subst $(DIRSRC), $(DIROBJ), $(patsubst %.cpp, %.o, $(wildcard $(DIRSRC)*.cpp)))\n'
        for folder in list_src:
            string += 'OBJS += $(subst $(DIRSRC' + folder.upper() + '), $(DIROBJ), $(patsubst %.cpp, %.o, $(wildcard $(DIRSRC' + folder.upper() + ')*.cpp)))\n'
        string += '\n.PHONY: all clean\n\n\
all: info $(EXEC)\n\n\
info:\n\
\t@echo ""\n\
\t@echo "--------------------------------"\n\
\t@echo "Building $(EXEC) in mode $(mode)"\n\
\t@echo "--------------------------------"\n\
\t@echo ""\n\n\
# Link ---------------------------------------------------------------\n\
$(EXEC): $(OBJS)\n\
\t@echo "Linking: $(notdir $^)"\n\
\t@$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS)\n\n\
\t@echo "Finished."\n\
# Compilation --------------------------------------------------------\n\
$(DIROBJ)%.o: $(DIRSRC)%.cpp\n\
\t@echo "Compiling: $(notdir $<)"\n\
\t@$(CXX) $(CXXFLAGS) -c $< -o $@ $(LDLIBS)'
        for folder in list_src:
            string += '\n\n$(DIROBJ)%.o: $(DIRSRC' + folder.upper() + ')%.cpp\n\
\t@echo "Compiling: $(notdir $<)"\n\
\t@$(CXX) $(CXXFLAGS) -c $< -o $@ $(LDLIBS)'
        string += '\n\n# Cleaning ---------------------------------------------\n\
clean:\n\
\trm -f *.log $(EXEC) *~ $(DIROBJ)* $(DIRSRC)*~'

        with open('makefile', 'w') as wfile:
            wfile.write(string)

if __name__ == '__main__':
    app = MyApp()
    app.run()
