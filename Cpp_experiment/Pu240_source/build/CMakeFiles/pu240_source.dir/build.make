# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build

# Include any dependencies generated for this target.
include CMakeFiles/pu240_source.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/pu240_source.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/pu240_source.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/pu240_source.dir/flags.make

CMakeFiles/pu240_source.dir/pu240_source.cpp.o: CMakeFiles/pu240_source.dir/flags.make
CMakeFiles/pu240_source.dir/pu240_source.cpp.o: /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/pu240_source.cpp
CMakeFiles/pu240_source.dir/pu240_source.cpp.o: CMakeFiles/pu240_source.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/pu240_source.dir/pu240_source.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/pu240_source.dir/pu240_source.cpp.o -MF CMakeFiles/pu240_source.dir/pu240_source.cpp.o.d -o CMakeFiles/pu240_source.dir/pu240_source.cpp.o -c /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/pu240_source.cpp

CMakeFiles/pu240_source.dir/pu240_source.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/pu240_source.dir/pu240_source.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/pu240_source.cpp > CMakeFiles/pu240_source.dir/pu240_source.cpp.i

CMakeFiles/pu240_source.dir/pu240_source.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/pu240_source.dir/pu240_source.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/pu240_source.cpp -o CMakeFiles/pu240_source.dir/pu240_source.cpp.s

# Object files for target pu240_source
pu240_source_OBJECTS = \
"CMakeFiles/pu240_source.dir/pu240_source.cpp.o"

# External object files for target pu240_source
pu240_source_EXTERNAL_OBJECTS =

libpu240_source.so: CMakeFiles/pu240_source.dir/pu240_source.cpp.o
libpu240_source.so: CMakeFiles/pu240_source.dir/build.make
libpu240_source.so: /usr/local/lib/libopenmc.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/hdf5/mpich/libhdf5.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libcrypto.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libcurl.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libsz.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libz.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/hdf5/mpich/libhdf5_hl.so
libpu240_source.so: /usr/local/lib/libfmt.a
libpu240_source.so: /usr/local/lib/libpugixml.a
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libpng.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libz.so
libpu240_source.so: /usr/lib/gcc/x86_64-linux-gnu/12/libgomp.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libpthread.a
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libmpichcxx.so
libpu240_source.so: /usr/lib/x86_64-linux-gnu/libmpich.so
libpu240_source.so: CMakeFiles/pu240_source.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library libpu240_source.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/pu240_source.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/pu240_source.dir/build: libpu240_source.so
.PHONY : CMakeFiles/pu240_source.dir/build

CMakeFiles/pu240_source.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/pu240_source.dir/cmake_clean.cmake
.PHONY : CMakeFiles/pu240_source.dir/clean

CMakeFiles/pu240_source.dir/depend:
	cd /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build /global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build/CMakeFiles/pu240_source.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/pu240_source.dir/depend

