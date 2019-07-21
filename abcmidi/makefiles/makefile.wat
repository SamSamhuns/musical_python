# Watcom Win32 Makefile for abcMIDI package 
# Use mingw or gnu standard make program with this makefile.
# 
#
# compilation #ifdefs - you may need to change these defined to get
#                       the code to compile with a different C compiler.
#
# NOFTELL in midifile.c and genmidi.c selects a version of the file-writing
#         code which doesn't use file seeking.
#
# PCCFIX in mftext.c midifile.c midi2abc.c
#        comments out various things that aren't available in PCC
#
# USE_INDEX causes index() to be used instead of strchr(). This is needed
#           by some pre-ANSI C compilers.
#
# ASCTIME causes asctime() to be used instead of strftime() in pslib.c.
#         If ANSILIBS is not set, neither routine is used.
#
# ANSILIBS causes code to include some ANSI standard headers
#
# KANDR selects functions prototypes without argument prototypes.
#
CC=wcc386
CFLAGS=-ic:\\watcom\\h;c:\\watcom\\h\\nt -w4 -e25 -zq -od -d2 -5r -bt=nt -mf -DANSILIBS
LDFLAGS=sys nt name 
LDFLAGS2=d all op inc op st=200000 op maxe=25 op q op symf 
LNK=wlink

all : abc2midi.exe midi2abc.exe abc2abc.exe mftext.exe yaps.exe midicopy.exe abcmatch.exe

abc2midi.exe : parseabc.obj store.obj genmidi.obj queues.obj midifile.obj parser2.obj stresspat.obj -lm
	$(LNK) $(LDFLAGS) abc2midi.exe $(LDFLAGS2) FILE parseabc.obj FILE genmidi.obj FILE store.obj \
	FILE queues.obj FILE midifile.obj FILE parser2.obj FILE stresspat.obj

abc2abc.exe : parseabc.obj toabc.obj
	$(LNK) $(LDFLAGS) abc2abc.exe $(LDFLAGS2) FILE parseabc.obj FILE toabc.obj 

midi2abc.exe : midifile.obj midi2abc.obj 
	$(LNK) $(LDFLAGS) midi2abc.exe $(LDFLAGS2) FILE midifile.obj FILE midi2abc.obj

mftext.exe : midifile.obj mftext.obj crack.obj
	$(LNK) $(LDFLAGS) mftext.exe $(LDFLAGS2) FILE midifile.obj FILE mftext.obj FILE crack.obj

midicopy.exe : midicopy.obj
	$(LNK) $(LDFLAGS) midicopy.exe $(LDFLAGS2) FILE midicopy.obj

yaps.exe : parseabc.obj yapstree.obj drawtune.obj debug.obj pslib.obj position.obj parser2.obj
	$(LNK) $(LDFLAGS) yaps.exe $(LDFLAGS2) FILE parseabc.obj FILE yapstree.obj FILE drawtune.obj FILE debug.obj FILE position.obj FILE pslib.obj FILE parser2.obj 


abcmatch.exe : abcmatch.obj matchsup.obj parseabc.obj
	$(LNK) $(LDFLAGS) abcmatch.exe $(LDFLAGS2) FILE abcmatch.obj FILE  matchsup.obj FILE parseabc.obj


# common parser object code
#
parseabc.obj : parseabc.c abc.h parseabc.h
	$(CC) $(CFLAGS) parseabc.c 

parser2.obj : parser2.c parseabc.h parser2.h
	$(CC) $(CFLAGS) parser2.c

# objects needed by abc2abc
#
toabc.obj : toabc.c abc.h parseabc.h
	$(CC) $(CFLAGS) toabc.c 

# objects needed by abc2midi
#
store.obj : store.c abc.h parseabc.h parser2.h genmidi.h 
	$(CC) $(CFLAGS) store.c 

genmidi.obj : genmidi.c abc.h midifile.h genmidi.h
	$(CC) $(CFLAGS) genmidi.c 

stresspat.obj : stresspat.c
	$(CC) $(CFLAGS) stresspat.c

# could use -DNOFTELL here
tomidi.obj : tomidi.c abc.h midifile.h
	$(CC) $(CFLAGS) tomidi.c

queues.obj: queues.c genmidi.h
	$(CC) $(CFLAGS) queues.c

# common midifile library
#
# could use -DNOFTELL here
midifile.obj : midifile.c midifile.h
	$(CC) $(CFLAGS) midifile.c

# objects needed by yaps
#
yapstree.obj: yapstree.c abc.h parseabc.h structs.h drawtune.h parser2.h
	$(CC) $(CFLAGS) yapstree.c

drawtune.obj: drawtune.c structs.h sizes.h abc.h drawtune.h
	$(CC) $(CFLAGS) drawtune.c

pslib.obj: pslib.c drawtune.h
	$(CC) $(CFLAGS) pslib.c

position.obj: position.c abc.h structs.h sizes.h
	$(CC) $(CFLAGS) position.c

debug.obj: debug.c structs.h abc.h
	$(CC) $(CFLAGS) debug.c

# objects needed by midi2abc
#
midi2abc.obj : midi2abc.c midifile.h
	$(CC) $(CFLAGS) midi2abc.c

# objects for mftext
#
crack.obj : crack.c
	$(CC) $(CFLAGS) crack.c 

mftext.obj : mftext.c midifile.h
	$(CC) $(CFLAGS) mftext.c

# objects for midicopy
#
midicopy.obj : midicopy.c midicopy.h
	$(CC) $(CFLAGS) midicopy.c

#objects for abcmtch
#
abcmatch.obj : abcmatch.c abc.h
	$(CC) $(CFLAGS) abcmatch.c

matchsup.obj : matchsup.c abc.h parseabc.h parser2.h genmidi.h
	$(CC) $(CFLAGS) matchsup.c

clean:
	rm *.obj
	rm *.exe

zipfile: midi2abc.exe abc2midi.exe mftext.exe yaps.exe abc2abc.exe abcmatch.exe
	zip pcexe2.zip *.exe readme.txt abcguide.txt demo.abc yaps.txt
