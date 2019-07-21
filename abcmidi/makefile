# Generic unix/gcc Makefile for abcMIDI package 
# 
#
# compilation #ifdefs - you need to compile with these defined to get
#                       the code to compile with PCC.
#
# NOFTELL in midifile.c and genmidi.c selects a version of the file-writing
#         code which doesn't use file seeking.
#
# PCCFIX in mftext.c midifile.c midi2abc.c
#        comments out various things that aren't available in PCC
#
# ANSILIBS includes some ANSI header files (which gcc can live without,
#          but other compilers may want).
#
# USE_INDEX causes index() to be used instead of strchr(). This is needed
#           by some pre-ANSI C compilers.
#
# ASCTIME causes asctime() to be used instead of strftime() in pslib.c.
#         If ANSILIBS is not set, neither routine is used.
#
# KANDR selects functions prototypes without argument prototypes.
#       currently yaps will only compile in ANSI mode.
#
#
# On running make, you may get the mysterious message :
#
# ', needed by `parseabc.o'. Stop `abc.h
#
# This means you are using GNU make and this file is in DOS text format. To
# cure the problem, change this file from using PC-style end-of-line (carriage 
# return and line feed) to unix style end-of-line (line feed).

CC=gcc
#CFLAGS=-DANSILIBS -O2 
CFLAGS+=-DANSILIBS -g 
LNK=gcc
INSTALL=install

prefix=/usr/local
binaries=abc2midi midi2abc abc2abc mftext yaps midicopy abcmatch

docdir=share/doc/abcmidi
bindir=bin
mandir=share/man/man1

all : abc2midi midi2abc abc2abc mftext yaps midicopy abcmatch

abc2midi : parseabc.o store.o genmidi.o midifile.o queues.o parser2.o stresspat.o
	$(LNK) $(CFLAGS) $(CPPFLAGS) $(LDFLAGS) -o abc2midi parseabc.o store.o genmidi.o queues.o \
	parser2.o midifile.o stresspat.o -lm

abc2abc : parseabc.o toabc.o
	$(LNK) $(LDFLAGS) -o abc2abc parseabc.o toabc.o

midi2abc : midifile.o midi2abc.o 
	$(LNK) $(LDFLAGS) midifile.o midi2abc.o -o midi2abc

mftext : midifile.o mftext.o crack.o
	$(LNK) $(LDFLAGS) midifile.o mftext.o crack.o -o mftext

yaps : parseabc.o yapstree.o drawtune.o debug.o pslib.o position.o parser2.o
	$(LNK) $(LDFLAGS) -o yaps parseabc.o yapstree.o drawtune.o debug.o \
	position.o pslib.o parser2.o -o yaps

midicopy : midicopy.o
	$(LNK) $(LDFLAGS) -o midicopy midicopy.o

abcmatch : abcmatch.o matchsup.o parseabc.o
	$(LNK) $(LDFLAGS) abcmatch.o matchsup.o parseabc.o -o abcmatch

parseabc.o : parseabc.c abc.h parseabc.h

parser2.o : parser2.c abc.h parseabc.h parser2.h

toabc.o : toabc.c abc.h parseabc.h

# could use -DNOFTELL here
genmidi.o : genmidi.c abc.h midifile.h genmidi.h

store.o : store.c abc.h parseabc.h midifile.h genmidi.h

queues.o : queues.c genmidi.h

# could use -DNOFTELL here
midifile.o : midifile.c midifile.h

midi2abc.o : midi2abc.c midifile.h

midicopy.o : midicopy.c midicopy.h

abcmatch.o: abcmatch.c abc.h

crack.o : crack.c

mftext.o : mftext.c midifile.h

# objects needed by yaps
#
yapstree.o: yapstree.c abc.h parseabc.h structs.h drawtune.h

drawtune.o: drawtune.c structs.h sizes.h abc.h drawtune.h

pslib.o: pslib.c drawtune.h

position.o: position.c abc.h structs.h sizes.h

debug.o: debug.c structs.h abc.h

#objects for abcmatch
#
matchsup.o : matchsup.c abc.h parseabc.h parser2.h

clean :
	-rm *.o ${binaries}

install: abc2midi midi2abc abc2abc mftext midicopy yaps abcmatch
	test -d $(DESTDIR)${prefix}/${bindir} || mkdir -p $(DESTDIR)${prefix}/${bindir}
	$(INSTALL) -m 755 ${binaries} $(DESTDIR)${prefix}/${bindir}

	# install documentation
	test -d $(DESTDIR)${PREFIX}/share/doc/abcmidi || mkdir -p $(DESTDIR)${prefix}/${docdir}
	$(INSTALL) -m 644 doc/*.txt $(DESTDIR)${prefix}/${docdir}
	$(INSTALL) -m 644 doc/AUTHORS $(DESTDIR)${prefix}/${docdir}
	$(INSTALL) -m 644 doc/CHANGES $(DESTDIR)${prefix}/${docdir}
	$(INSTALL) -m 644 VERSION $(DESTDIR)${prefix}/${docdir}

	# install manpages
	test -d $(DESTDIR)${prefix}/${mandir} || mkdir -p $(DESTDIR)${prefix}/${mandir};
	$(INSTALL) -m 644 doc/*.1 $(DESTDIR)${prefix}/${mandir}

