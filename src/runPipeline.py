#!python

import os, sys, string, time, BaseHTTPServer, getopt, re, subprocess, webbrowser
from operator import itemgetter

openbrowser = False
if os.environ.get('DISPLAY') != None:
    openbrowser = True
PREFIX = "proba"
VERBOSE = False
OSTYPE        = "Linux"
OSVERSION     = "0.0"
MACHINETYPE   = "x86_64"

METAMOSDIR    = sys.path[0]
METAMOS_UTILS = "%s%sUtilities"%(METAMOSDIR, os.sep) 
METAMOS_JAVA  = "%s%sjava:%s"%(METAMOS_UTILS,os.sep,os.curdir)

AMOS          = "%s%sAMOS%sbin"%(METAMOSDIR, os.sep, os.sep)

SOAP          = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
METAIDBA      = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
CA            = "%s%sCA%s%s-%s%sbin"%(METAMOSDIR, os.sep, os.sep, OSTYPE, MACHINETYPE.replace("x86_64", "amd64"), os.sep)
NEWBLER       = "%s%snewbler%s%s-%s"%(METAMOSDIR, os.sep, os.sep, OSTYPE, MACHINETYPE)
VELVET        = "%s%scpp%s%s-%s%svelvet"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE, os.sep)
VELVET_SC     = "%s%scpp%s%s-%s%svelvet-sc"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE, os.sep)

BOWTIE        = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)

GMHMMP        = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)

FCP           = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
PHMMER        = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
BLAST         = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
AMPHORA       = "%s%sAmphora-2"%(METAMOSDIR, os.sep)

KRONA         = "%s%skrona"%(METAMOS_UTILS,os.sep)
REPEATOIRE    = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)

libcounter = 1
readcounter = 1
t1 = time.time()
sys.path.append(METAMOS_UTILS)
from ruffus import *


class Read:
    format = ""
    maxlen = 150
    qformat = "Sanger"
    filtered = False
    mated = True
    path = ""
    fname = ""
    id = 0
    sid = ""
    def __init__(self,format,path,mated=True,interleaved=False):
        global readcounter 
        self.id = readcounter
        readcounter +=1
        self.format = format
        self.path = path
        self.fname = os.path.basename(self.path)
        self.mated = mated
        self.interleaved = interleaved
        #self.init()
        #self.validate()

class readLib:
    format = ""
    mean = 0
    stdev = 0
    mmin = 0
    mmax = 0
    mated = True
    interleaved = False
    innie = True
    linkerType = "titanium"
    frg = ""
    f1 = ""
    f2 = ""
    f12 = ""
    reads = []
    readDict = {}
    pairDict = {}
    def __init__(self,format,mmin,mmax,f1,f2="",mated=True,interleaved=False,innie=True,linkerType="titanium"):
        global libcounter
        self.id = libcounter
        self.sid = "lib"+str(libcounter)
        libcounter +=1
        self.format = format
        self.mated=mated
        self.interleaved=interleaved
        self.innie=innie
        self.linkerType=linkerType
        self.mmin = mmin
        self.mmax = mmax
        self.f1 = f1
        self.f2 = f2
        self.f1.sid = self.sid
        self.readDict[f1.id] = self.f1
        if f2 != "":
            self.readDict[f2.id] = self.f2
            self.pairDict[f1.id] = f2.id
            self.pairDict[f2.id] = f1.id
            self.f2.sid = self.sid
        self.reads.append(f1)
        if self.f2 != "":
            self.reads.append(f2)
        self.initLib()
        self.validateLib()
    def getPair(self,readId):
        try:
            return self.readDict[self.pairDict[readId]]
        except KeyError:
            #no pair for read
            return -1
    def initLib(self):
        self.mean = (self.mmin+self.mmax)/2.0
        self.stdev = 0.1*self.mean
        #count num reads
        #check pairs
        #if self.interleaved:
        #    f12 = self.f1.path
        #else:
        #need to shuffle em
        #    if self.f1.format == "fasta" and self.f2.format == "fasta":
        #        pass
        #    elif self.f2.format = "fastq" and self.f1.format == "fastq":
        #        pass
        #    f12 = ""
    def validateLib(self):
        pass

    def concatLib(self):
        #combine two libs of same format & w/ same insert size into one 
        pass
   
    def toggleInterleaved(self):
        #if interleaved switch to two files, else vice versa
        pass

    def filterReads(self):
        #remove all Reads with N, etc
        pass

    def __str__(self):
        pass




def concatContig(ctgfile):
    if len(sys.argv) < 3:
        print "usage: contig_file out_file"
    contig_file = open(ctgfile,'r')
    out_file = open(ctgfile+".merged",'w')
    out_data = ""
    for line in contig_file.xreadlines():
        if ">" not in line:
             out_data += line.replace("\n","")
    width = 60
    pp = 0
    out_file.write(">seq\n")
    while pp+60 < len(out_data):
        out_file.write(out_data[pp:pp+60]+"\n")
        pp +=60
    out_file.write(out_data[pp:]+"\n")
    out_file.close()
    contig_file.close()



def getContigRepeats(contigFile,outFile):

    contig_repeats = ""
    contig_file = ""
    try:
        contig_repeats = open(outFile,'w')
    except IOError, errmsg:
        print "Error creating output file %s "%(sys.argv[2]), errmsg
        sys.exit(1)

    try:
        contig_file = open(contigFile,'r')
    except IOError, errmsg:
        print "Error opening input file %s "%(sys.argv[1]), errmsg
        sys.exit(1)
    contig_file.close()
    contig_file = open(contigFile,'r')
    concatContig(contigFile)
    run_process("%s --minreplen=200 --z=17 --sequence=%s.merged --xmfa=%s.xmfa"%(REPEATOIRE,contigFile,contigFile),"FindRepeats")
    repeat_file = open(contigFile+".xmfa",'r')
    ctg_dict = {}
    seq_map = {}
    contig_data = contig_file.read()
    num_contigs = contig_data.count(">")
    contig_data = contig_data.split(">")[1:]
    prev_pos = 0
    eid = ""
    iid = 1
    for contig in contig_data:
        hdr,seq = contig.split("\n",1)
        id = hdr.split(" ")[0]
        hdr = hdr.replace(">","").replace("\n","")
        start = prev_pos
        clen = len(seq.replace("\n",""))
        end = prev_pos+clen
        ctg_dict[iid] = [start, end, seq]
        i = 0
        while i < clen:
            seq_map[prev_pos+i] = hdr#iid
            i+=1
        prev_pos = end+1
        iid +=1

    repeat_data = repeat_file.readlines()
    repfam = 1
    reppos = []
    clc = 1
    for line in repeat_data:
        if "=" in line:
          repfam +=1
          ctg_list = []
          for copy in reppos:
             try:
                #print seq_map[int(copy[0])]
                if seq_map[int(copy[0])] == seq_map[int(copy[1])]:
                    ctg_list.append(seq_map[int(copy[0])])
                    #ctg_list.append(seq_map[copy[1]])
             except KeyError:
                 continue
          #print ctg_list

          if len(ctg_list) > 1 and ctg_list.count(ctg_list[0]) != len(ctg_list):
              for item in ctg_list:
                   contig_repeats.write("%d:"%repfam+str(item)+"\n")
          clc +=1
          reppos = []
        if ">" not in line:
            continue
        gg, info = line.split(":",1)
        spos,info = info.split("-",1)
        epos,info = info.split(" ",1)
        orient, info = info.split(" ",1)
#        print spos, epos, orient
        reppos.append([spos,epos])



     
def parseInterleaved(rf,wf,fastq=True):
    if 1:
        if 1:
            if 1:
                   #this means we have this entire lib in one file
                   #parse out paired record (8 lines), rename header to be filename + "/1" or "/2", and remove reads with N
                   rf = open(read.path,'r')
                   wf = open(read.path.replace("/in/","/out/"),'w')
                   start = 1
                   rcnt = 0
                   recordcnt = 0
                   record = []
                   shdr = ""
                   for line in rf.xreadlines():
                       if start:
                           s1hdr = line
                           record.append(line)
                           start = 0
                           rcnt =1

                       else:
                           if rcnt == 7:
                               #end of record
                               record.append(line)
                               rcnt +=1
                               if len(record) != 8:
                                   #something went wrong
                                   continue
                               rseq = string.upper(record[0]+record[5])                               
                               if "N" in rseq:
                                   #skip both, dont' want Ns
                                   continue
                               #update hdrs to be filename /1 or /2
                               recordcnt +=1
                               hdr = read.sid+"r"+str(recordcnt)+"/"
                               #hdr2 = lib.sid[0:3]+str(int(lib.sid[3:])+1)+str(recordcnt)+"/"
                               if fastq == True:
                                   wf.writelines("@"+hdr+"1\n")
                                   wf.writelines(record[1])
                                   wf.writelines("+"+hdr+"1\n")
                                   wf.writelines(record[3])
                                   wf.writelines("@"+hdr+"2\n")
                                   wf.writelines(record[5])
                                   wf.writelines("+"+hdr+"2\n")
                                   wf.writelines(record[7])
                               else:
                                   wf.writelines(">"+hdr+"1\n")
                                   wf.writelines(record[1])
                                   wf.writelines(">"+hdr+"1\n")
                                   wf.writelines(record[3])
                                   wf.writelines(">"+hdr+"2\n")
                                   wf.writelines(record[5])
                                   wf.writelines(">"+hdr+"2\n")
                                   wf.writelines(record[7])
                           elif rcnt % 4 == 0:
                               s2hdr = line
                               rlcs = LCS(s1hdr,s2hdr)
                               #these should almost identical
                               if float(len(rlcs))/float(len(s1hdr)) < 0.9:
                                   #missing record somewhere, start over with this one
                                   s1hdr = line
                                   record = [line]
                                   start = 0
                                   rcnt = 1
                               else:
                                   record.append(line)
                                   rcnt +=1
                           elif rcnt % 2 == 0:
                               #quality hdr
                               record .append(line)
                               rcnt +=1
                           else:
                               record .append(line)
                               rcnt +=1
                   #update to new path
                   read.path = read.path.replace("/in/","/out/")            


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def getMachineType():
   global OSTYPE
   global OSVERSION
   global MACHINETYPE

   p = subprocess.Popen("echo `uname`", shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   (checkStdout, checkStderr) = p.communicate()
   if checkStderr != "":
      print "Warning: Cannot determine OS, defaulting to %s"%(OSTYPE)
   else:
      OSTYPE = checkStdout.strip()

   p = subprocess.Popen("echo `uname -r`", shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   (checkStdout, checkStderr) = p.communicate()
   if checkStderr != "":
      print "Warning: Cannot determine OS version, defaulting to %s"%(OSVERSION)
   else:
      OSVERSION = checkStdout.strip()

   p = subprocess.Popen("echo `uname -m`", shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   (checkStdout, checkStderr) = p.communicate()
   if checkStderr != "":
      print "Warning: Cannot determine system type, defaulting to %s"%(MACHINETYPE)
   else:
      MACHINETYPE = checkStdout.strip()

def getFromPath(theCommand, theName):
    p = subprocess.Popen("which %s"%(theCommand), shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (checkStdout, checkStderr) = p.communicate()
    if checkStderr != "":
       print "Warning: %s is not found, some functionality will not be available"%(theName)
       return ""
    else:
       return checkStdout.replace(theCommand, "").strip()

def guessPaths():
    global METAMOSDIR
    global METAMOS_UTILS
    global METAMOS_JAVA
    global AMOS
    global SOAP
    global METAIDBA
    global REPEATOIRE
    global CA
    global NEWBLER
    global VELVET
    global VELVET_SC
    global BOWTIE
    global GMHMMP
    global FCP
    global PHMMER
    global BLAST
    global AMPHORA

    getMachineType()

    if not os.path.exists(METAMOS_UTILS):
       METAMOSDIR = sys.path[0]
       print "Script is running from: %s"%(METAMOSDIR)
   
       METAMOS_UTILS = "%s%sUtilities"%(METAMOSDIR, os.sep) 
       if not os.path.exists(METAMOS_UTILS):
          print "Error: cannot find metAMOS utilities. Will not run pipeline"
          sys.exit(1);   

       METAMOS_JAVA  = "%s%sjava:%s"%(METAMOS_UTILS, os.sep, os.curdir)

    # now check for assemblers
    # 1. AMOS
    AMOS = "%s%sAMOS%s%s-%s%sbin"%(METAMOSDIR, os.sep, os.sep, OSTYPE, MACHINETYPE, os.sep)
    if not os.path.exists(AMOS + os.sep + "toAmos_new"):
       AMOS = getFromPath("toAmos_new", "AMOS") 
       if not os.path.exists(AMOS + os.sep + "toAmos_new"):
          print "Error: cannot find AMOS in %s or %s. Please check your path and try again."%(METAMOSDIR + os.sep + "AMOS", AMOS)
          sys.exit(1)
    # 2. Soap
    SOAP = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE) 
    if not os.path.exists(SOAP + os.sep + "SOAPdenovo-63mer"):
       SOAP = getFromPath("SOAPdenovo-63mer", "SOAP")
    # 3. CA
    CA = "%s%sCA%s%s-%s%sbin"%(METAMOSDIR, os.sep, os.sep, OSTYPE, MACHINETYPE.replace("x86_64","amd64"), os.sep)
    if not os.path.exists(CA + os.sep + "gatekeeper"):
       CA = getFromPath("gatekeeper", "Celera Assembler") 
    # 4. Newbler
    NEWBLER = "%s%snewbler"%(METAMOSDIR, os.sep);
    if not os.path.exists(NEWBLER + os.sep + "runProject"):
       NEWBLER = getFromPath("runProject", "Newbler")

    # 5. meta-IDBA
    METAIDBA = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE) 
    if not os.path.exists(METAIDBA + os.sep + "metaidba"):
       METAIDBA = getFromPath("metaidba", "METAIDBA")

    # when searching for velvet, we ignore paths because there are so many variations of velvet (velvet, velvet-sc, meta-velvet that all have a velveth/g and we have no way to tell if we got the right one
    #6. velvet
    VELVET = "%s%scpp%s%s-%s%svelvet"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE, os.sep);
    if not os.path.exists(VELVET + os.sep + "velvetg"):
       VELVET = ""
    #7. velvet-sc
    VELVET_SC = "%s%scpp%s%s-%s%svelvet-sc"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE, os.sep);
    if not os.path.exists(VELVET_SC + os.sep + "velvetg"):
       VELVET_SC = ""

    # now for repeatoire
    REPEATOIRE = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
    if not os.path.exists(REPEATOIRE + os.sep + "repeatoire"):
       REPEATOIRE = getFromPath("repeatoire", "Repeatoire")
    else:
       REPEATOIRE += os.sep + "repeatoire"
    # now for the mappers
    BOWTIE = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
    if not os.path.exists(BOWTIE + os.sep + "bowtie"):
       BOWTIE = getFromPath("bowtie", "Bowtie")

    # now for the annotation
    GMHMMP = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
    if not os.path.exists(GMHMMP + os.sep + "gmhmmp"):
       GMHMMP = getFromPath("gmhmmp", "GeneMark.hmm")

    FCP = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
    if not os.path.exists(FCP + os.sep + "fcp"):
       FCP = getFromPath("fcp", "FCP")
    PHMMER = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
    if not os.path.exists(PHMMER + os.sep + "phmmer"):
       PHMMER = getFromPath("phmmer", "PHmmer")
    BLAST = "%s%scpp%s%s-%s"%(METAMOS_UTILS, os.sep, os.sep, OSTYPE, MACHINETYPE)
    if not os.path.exists(BLAST + os.sep + "blastall"):
       BLAST = getFromPath("blastall", "blast")
    # currently only supported on Linux 64-bit and only from one location
    AMPHORA = "%s%sAmphora-2"%(METAMOSDIR, os.sep)
    if not os.path.exists(AMPHORA + os.sep + "amphora2"):
       print "Warning: Amphora 2 was not found, will not be available\n";
       AMPHORA = ""
    if AMPHORA != "" and (OSTYPE != "Linux" or MACHINETYPE != "x86_64"):
       print "Warning: Amphora 2 not compatible with %s-%s. It requires Linux-x86_64\n"%(OSTYPE, MACHINETYPE)
       AMPHORA = "" 

    # finally add the utilities to our path
    print "Configuration summary:"
    print "OS:\t\t\t%s\nOS Version:\t\t%s\nMachine:\t\t%s\n"%(OSTYPE, OSVERSION, MACHINETYPE)
    print "metAMOS main dir:\t%s\nmetAMOS Utilities:\t%s\nmetAMOS Java:\t\t%s\n"%(METAMOSDIR, METAMOS_UTILS, METAMOS_JAVA)
    print "AMOS:\t\t\t%s\nSOAP:\t\t\t%s\nMETAIDBA:\t\t%s\nCelera Assembler:\t%s\nNEWBLER:\t\t%s\n"%(AMOS, SOAP, METAIDBA,CA, NEWBLER)
    print "Velvet:\t\t\t%s\nVelvet-SC:\t\t%s\n"%(VELVET, VELVET_SC)
    print "Bowtie:\t\t\t%s"%(BOWTIE)
    print "GMHMMP:\t\t\t%s"%(GMHMMP)
    print "FCP:\t\t\t%s"%(FCP)
    print "PHMMER:\t\t\t%s"%(PHMMER)
    print "BLAST:\t\t\t%s"%(BLAST)
    print "AMPHORA:\t\t%s"%(AMPHORA)

    print "REPEATOIRE:\t\t%s"%(REPEATOIRE)

def run_process(command,step=""):
       outf = ""
       workingDir = ""
       if step != "":
           workingDir = "%s/%s/out"%(rundir, step)
           if not os.path.exists(workingDir):
              workingDir = ""
           step = string.upper(step)
           if not os.path.exists(rundir+"/Logs"):
               os.system("mkdir %s/Logs"%(rundir))
           outf = open(rundir+"/Logs/"+step+".log",'a')
       if VERBOSE:
           print command
       stdout = ""
       stderr = ""
       if workingDir == "":
           p = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE,close_fds=True,executable="/bin/bash")
       else:
           p = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE,close_fds=True,executable="/bin/bash", cwd=workingDir)
       fstdout,fstderr = p.communicate()

       if step == "":
           print fstdout,fstderr
       else:
           outf.write(fstdout+fstderr)
           outf.close()


def getProgramParams(fileName, module="", prefix="", comment="#"):
    # we process parameters in the following priority:
    # first: current directory
    # second: user home directory
    # third: metAMOS directory
    # a parameter specifeid in the current directory takes priority over all others, and so on down the line
    dirs = [METAMOS_UTILS + os.sep + "config", os.path.expanduser('~') + os.sep + ".metAMOS", os.getcwd()]
    optDict = {} 

    cmdOptions = ""

    for curDir in dirs:
       curFile = curDir + os.sep + fileName;
       try:
          spec = open(curFile, 'r')
       except IOError as e:
          continue

       read = False
       if module == "":
          read = True

       for line in spec:
          (line, sep, commentLine) = line.partition(comment)
          line = line.strip()

          if line == "[" + module + "]":
             read = True
             continue;
          elif read == True and line.startswith("["):
             break;

          if read:
             if (line != ""):
                splitLine = line.split();
                optDict[splitLine[0]] = "".join(splitLine[1:]).strip() 
       spec.close()

    for option in optDict:
       cmdOptions += prefix + option + " " + optDict[option] + " ";

    return cmdOptions

def usage():
    print "usage: runPipeline.py [options] -d projectdir (required)"
    print "options:  -a <assembler> -k <kmer size> -c <classification method> -m <enable metaphyler?> -p <num threads>  "
    print "-h: help?"
    print "-r: retain the AMOS bank?  (default = NO)"
    print "-b: use bowtie for read mapping? (default = NO)"
    print "-d = <project dir>: directory created by initPipeline"
    print "-s = <runPipeline step>: start at this step in the pipeline"
    print "-e = <runPipeline step>: end at this step in the pipeline"
    print "-o = <int>>: min overlap length"
    print "-k = <int>: kmer size for assembly"
    print "-c = <classifier>: classifier to use for annotation"
    print "-a = <assembler>: genome assembler to use"
    print "-n = <runPipeline step>: step to skip in pipeline"
    print "-p = <int>: number of threads to use (be greedy!)"
    print "-t: filter input reads? (default = NO)"
    print "-f = <runPipeline step>: force this step to be run"
    print "-v: verbose output? (default = NO)"
    print "-m: use metaphyler? (default = YES)"
    print "-4: 454 data? (default = NO)"
    
    #print "options: annotate, stopafter, startafter, fq, fa"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hrbd:s:e:o:k:c:a:n:p:tf:vm4", ["help", "retainBank""bowtie","projectdir","startat","endat", "minoverlap","kmersize","classifier","assembler","skipsteps","threads","filter","forcesteps","verbose","metaphyler","454"])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

allsteps = ["Preprocess","Assemble","FindORFS","Abundance","Annotate","Scaffold","Propagate","Classify","Postprocess"]
output = None
reads = None
quals = None
format = None
verbose = False
bowtie_mapping = 1
startat = None
stopat = None
filter = False
forcesteps = []
skipsteps = []
run_metaphyler = False
runfast = False
cls = None
retainBank = False
asm = "none"
rundir = ""
fff = ""
threads = 16
readlen = 75
kmer = 31
fqlibs = {}
fqfrags = []
rlibs = []
for o, a in opts:
    if o in ("-v","--verbose"):
        VERBOSE = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-b","--bowtie"):
        bowtie_mapping = 1
    elif o in ("-s","--startat"):
        startat = a
        if startat not in allsteps:
            print "cannot start at %s, step does not exist in pipeline"%(startat)
            print allsteps 
    elif o in ("-e","--endat"):
        pass
    elif o in ("-o", "--minoverlap"):
        pass
    elif o in ("-k", "--kmersize"):
        kmer = int(a)
    elif o in ("-4", "--454"):
        fff = "-454"
    elif o in ("-f", "--forcesteps"):
        #print o,a
        forcesteps = a.split(",")
        #print forcesteps
    elif o in ("-n", "--skipsteps"):
        #print o, a
        skipsteps = a.split(",")
        #print skipsteps
    elif o in ("-p", "--threads"):
        threads = int(a)
    elif o in ("-d", "--projectdir"):
        rundir = os.path.abspath(a)
        if not os.path.exists(a):
          print "project dir %s does not exist!"%(rundir)
          usage()
          sys.exit(1)
    elif o in ("-t", "--filter"):
        filter = True

    elif o in ("-m", "--metaphyler"):
        run_metaphyler = True
    elif o in ("-r", "--retainBank"):
        retainBank = True
    elif o in ("-c", "--classifier"):
        #blast,fcp,etc 
        #default: fcp?
        cls = a#"phmmer"
        if cls == "amphora2" or cls == "Amphora2":
            cls = "amphora"
    elif o in ("-a","--assembler"):
        #maximus,CA,soap
        #default: maximus?
        asm = a
        if asm == "metaidba":
            bowtie_mapping = 1
    elif o in ("-f","--fastest"):
        #tweak all parameters to run fast
        #bambus2, use SOAP, etc
        runfast = True
    
    else:
        assert False, "unhandled option"

    #sys.exit(2)

if not os.path.exists(rundir) or rundir == "":
    print "project dir %s does not exist!"%(rundir)
    usage()
    sys.exit(1)

#parse frag/libs out of pipeline.ini out of rundir
inifile = rundir+os.sep+"pipeline.ini"
inf = open(inifile,'r')
libs = []
readlibs = []
readobjs = []
frgs = []
format = ""
mean = 0
stdev = 0
mmin = 0
mmax = 0
mated = True
interleaved = False
innie = True
linkerType = "titanium"
frg = ""
f1 = ""
f2 = ""
currlibno = 0
newlib = ""
libadded = False
for line in inf:
    line = line.replace("\n","")
    if "#" in line:
        continue
    elif "asmcontigs:" in line:
        #move to proba.asm.contigs
        #skip Assembly
        asmc = line.replace("\n","").split("\t")[-1]
        if len(asmc) <= 2:
            continue
        run_process("mv %s %s/Assemble/out/%s"%(asmc,rundir,"proba.asm.contig"))
        #skipsteps.append("Assemble")
        asm = "none"
        bowtie_mapping = 1
    elif "format:" in line:

        if f1 and not libadded:
            nread1 = Read(format,f1,mated,interleaved)
            readobjs.append(nread1)
            nread2 = ""
            nlib = readLib(format,mmin,mmax,nread1,nread2,mated,interleaved,innie,linkerType)
            readlibs.append(nlib)
        libadded = False
        format = line.replace("\n","").split("\t")[-1]
    elif "mated:" in line:
        mated = str2bool(line.replace("\n","").split("\t")[-1])
    elif "interleaved:" in line:
        interleaved = str2bool(line.replace("\n","").split("\t")[-1])
    elif "innie:" in line:
        innie = str2bool(line.replace("\n","").split("\t")[-1])
    elif "linker:" in line:
        linkerType = line.replace("\n","").split("\t")[-1]
    elif "f1:" in line:# or "f2:" in line:
        data = line.split("\t")

        fqlibs[data[0]] = data[1]
        #f1 = data[1].split(",")[0]
        f1 = "%s/Preprocess/in/%s"%(rundir,data[1].split(",")[0])
        inf = data[1].split(",")
        mean = int(inf[3])
        stdev = int(inf[4])
        mmin = int(inf[1])
        mmax = int(inf[2])
        libs.append(f1)

    elif "f2:" in line:# or "f2:" in line:
        data = line.split("\t")

        fqlibs[data[0]] = data[1]
        f2 = "%s/Preprocess/in/%s"%(rundir,data[1].split(",")[0])
        inf = data[1].split(",")
        mean = int(inf[3])
        stdev = int(inf[4])
        mmin = int(inf[1])
        mmax = int(inf[2])
        libs.append(f2)
        
        nread1 = Read(format,f1,mated,interleaved)
        readobjs.append(nread1)
        nread2 = Read(format,f2,mated,interleaved)
        readobjs.append(nread2)
        nlib = readLib(format,mmin,mmax,nread1,nread2,mated,interleaved,innie,linkerType)
        readlibs.append(nlib)
        libadded = True
    elif "frg" in line:

        data = line.split("\t")
        frg = data[1]
        mated = False
        f1 = frg
        #fqfrags[data[0]] = data[1]
        #frgs.append(data[1])
        libs.append(frg)
if f1 and not libadded:
    nread1 = Read(format,f1,mated,interleaved)
    readobjs.append(nread1)
    nread2 = ""
    nlib = readLib(format,mmin,mmax,nread1,nread2,mated,interleaved,innie,linkerType)
    readlibs.append(nlib)
    #libadded = True


if len(readlibs) > 1 and asm == "metaidba":
    print "ERROR: meta-IDBA only supports 1 library, please select different assembler or reduce libraries"
    sys.exit(1)

def map2contig():
    #bowtie_mapping = 1
    
    readDir = ""
    asmDir = ""
    #threads = 0
    tigr_file = open("%s/Assemble/out/%s.asm.tigr"%(rundir,PREFIX),'w')
    contigfile = open("%s/Assemble/out/%s.asm.contig"%(rundir,PREFIX),'r')

    seqdict = {}
    hdr = ""
    cnt = 0
    contigdict = {}
    contigdict2 = {}
    readdict = {}
    matedict = {}
    ctgmates = 0
    matectgdict = {}
    mateotdict = {}
    read_lookup = {}
    readcnt = 1

    for lib in readlibs:
         

        matefile = open("%s/Preprocess/out/lib%d.seq.mates"%(rundir,lib.id),'r')
        matedict[lib.id] = {}
        for line in matefile.xreadlines():
            line = line.replace("\n","")
            mate1, mate2 = line.split("\t")
            mate1 = mate1.replace("@","").replace(">","")
            mate2 = mate2.replace("@","").replace(">","")
            matedict[lib.id][mate2] = mate1
            #matedict[lib.id][mate1] = mate2
            read_lookup[readcnt] = mate1
            read_lookup[readcnt+1] = mate2
            readcnt += 2
    if bowtie_mapping == 1:
        for lib in readlibs:
            seqfile = open("%s/Preprocess/out/lib%d.seq.btfilt"%(rundir,lib.id),'w')


            #trim to 25bp
            trim = 0
            if trim:
                f1 = open("%s/Preprocess/out/lib%d.seq"%(rundir,lib.id))
                f2 = open("%s/Preprocess/out/lib%d.seq.trim"%(rundir,lib.id),'w')
                linecnt = 1
                for line in f1.xreadlines():
                    if linecnt % 2 == 0:
                        f2.write(line[0:25]+"\n")
                    else:
                        f2.write(line)
                    linecnt +=1
                f1.close()
                f2.close()
            if not os.path.exists("%s/Assemble/out/IDX.1.ebwt"%(rundir)):
                run_process("%s/bowtie-build %s/Assemble/out/%s.asm.contig %s/Assemble/out/IDX"%(BOWTIE, rundir,PREFIX,rundir),"Scaffold")
            #run_process("%s/bowtie-build %s/Assemble/out/%s.asm.contig %s/Assemble/out/IDX"%(BOWTIE, rundir,PREFIX,rundir))
            if "bowtie" not in skipsteps and (lib.format == "fasta" or lib.format == "sff"):
                if trim:
                    run_process("%s/bowtie -p %d -f -v 1 -M 2 %s/Assemble/out/IDX %s/Preprocess/out/lib%d.seq.trim &> %s/Assemble/out/%s.bout"%(BOWTIE,threads,rundir,rundir,lib.id,rundir,PREFIX),"Scaffold")
                else:
                    run_process("%s/bowtie -p %d -f -l 28 -M 2 %s/Assemble/out/IDX %s/Preprocess/out/lib%d.seq &> %s/Assemble/out/%s.bout"%(BOWTIE,threads,rundir,rundir,lib.id,rundir,PREFIX))
            elif "bowtie" not in skipsteps and lib.format != "fasta":
                if trim:
                    run_process("%s/bowtie  -p %d -v 1 -M 2 %s/Assemble/out/IDX %s/Preprocess/out/lib%d.seq.trim &> %s/Assemble/out/%s.bout"%(BOWTIE,threads,rundir,rundir,lib.id,rundir,PREFIX),"Scaffold")
                else:
                    run_process("%s/bowtie  -p %d -l 28 -M 2 %s/Assemble/out/IDX %s/Preprocess/out/lib%d.seq &> %s/Assemble/out/%s.bout"%(BOWTIE,threads,rundir,rundir,lib.id,rundir,PREFIX),"Scaffold")
            infile = open("%s/Assemble/out/%s.bout"%(rundir,PREFIX),'r')
            for line1 in infile.xreadlines():
                line1 = line1.replace("\n","")
                ldata = line1.split("\t")
                if len(ldata) < 6:
                    continue
                read = ldata[0]
                strand = ldata[1]
                contig = ldata[2]
                spos = ldata[3] 
                read_seq = ldata[4]
                read_qual = ldata[5]
                read = read.split(" ")[0]
                epos = int(spos)+len(read_seq)
                try:
                    contigdict[contig].append([int(spos), int(spos)+epos, strand, read])
                except KeyError:
                    contigdict[contig] = [[int(spos),int(spos)+epos,strand,read]]
            
                seqdict[read] = read_seq
                seqfile.write(">%s\n%s\n"%(read,read_seq))
                seqfile.flush()
    else:
        if 1:
 
            #open soap ReadOnContig
            #some contigs are missing!
            infile = open("%s/Assemble/out/%s.asm.readOnContig"%(rundir,PREFIX),'r')
            #readID, ContigID, startpos, strand
            hdr = infile.readline()
            linecnt = 1
            for line in infile.xreadlines():
                if linecnt % 100000 == 0:
                    #print linecnt,
                    sys.stdout.flush()
                data = line.replace("\n","").split("\t")
                #print data
                if len(data) < 4:
                    continue
                contig = data[1]
                spos = int(data[2])
                if spos < 0:
                    spos = 0
                epos = spos+readlen
                strand = data[3]
                read = int(data[0])

                try:
                    contigdict[contig].append([int(spos), int(spos)+epos, strand, read_lookup[read]])
                except KeyError:
                    contigdict[contig] = [[int(spos),int(spos)+epos,strand,read_lookup[read]]]
                read_seq = "TEST"
            
                seqdict[read_lookup[read]] = read_seq
                linecnt +=1
        
    contig_data = contigfile.read()
    contig_data = contig_data.split(">")
    errfile = open("%s/Assemble/out/contigs_wo_location_info.txt"%(rundir),'w')
    new_ctgfile = open("%s/Assemble/out/%s.seq100.contig"%(rundir,PREFIX),'w')
    ctgcnt = 1
    ctgseq = 0
    ctgsizes = []
    n50_size = 0
    n50_mid = 955,000
    ctg_cvg_file = open("%s/Assemble/out/%s.contig.cvg"%(rundir,PREFIX),'w')
    for item in contig_data:
        if item == '':
            continue

        item = item.split("\n",1)
        ref = item[0].split(" ")[0]
        ref = ref.replace("\n","")
        cseq = item[1].replace("\n","")
        ctgseq+=len(cseq)
        ctgsizes.append(len(cseq))
        i = 0
        cpos = 0
        width = 70
        cseq_fmt = ""
        while i+width < len(cseq):
            cseq_fmt += cseq[i:i+width]+"\n"
            i+= width
        cseq_fmt += cseq[i:]+"\n"
        ctgslen = len(item[1])
        #contigdict2[ref] = item[1]
        try:
            tigr_file.write("##%s %d %d bases, 00000000 checksum.\n"%(ref.replace(">",""),len(contigdict[ref]), len(item[1])))
            tigr_file.flush()
        except KeyError:
            #print "oops, not in mapping file\n"
            errfile.write("%s\n"%ref)
            continue
        new_ctgfile.write(">%d\n%s"%(ctgcnt,cseq_fmt))#item[1]))
        ctgcnt +=1
        tigr_file.write(cseq_fmt)#item[1])
        contigdict[ref].sort()
        #print contigdict[ref]
        ctg_cvg_file.write("%s\t%.2f\n"%(ref,(float(len(contigdict[ref])*len(seqdict[contigdict[ref][0][-1]]))/float(ctgslen))))
        for read in contigdict[ref]:
            
            try:
                #if read[0] <= 500 and ctgslen - (int(read[1])) <= 500:
                matectgdict[read[-1]] = ref
                mateotdict[read[-1]] = read[2]
            except KeyError:
                pass
            if read[2] == "-":
                tigr_file.write("#%s(%d) [RC] %d bases, 00000000 checksum. {%d 1} <%d %s>\n"%(read[-1],read[0]-1, len(seqdict[read[-1]]), len(read[-1]), read[0], read[1]))
            else:
                tigr_file.write("#%s(%d) [] %d bases, 00000000 checksum. {1 %d} <%d %s>\n"%(read[-1],read[0]-1, len(seqdict[read[-1]]), len(read[-1]), read[0], read[1]))
            tigr_file.write(seqdict[read[-1]]+"\n")

   

    for lib in readlibs:
        new_matefile = open("%s/Assemble/out/%s.lib%d.mappedmates"%(rundir,PREFIX,lib.id),'w')
        new_matefile.write("library\t%d\t%d\t%d\n"%(lib.id,lib.mmin,lib.mmax))
        #    for lib in readlibs:
        linked_contigs = {}
        for mate in matedict[lib.id].keys():
            new_matefile.write("%s\t%s\t%d\n"%(mate,matedict[lib.id][mate],lib.id))
            new_matefile.flush()
            continue
    ctg_cvg_file.close()
    tigr_file.close()

def extractNewblerReads():
   run_process("unlink %s/Preprocess/out/all.seq.mates"%(rundir), "Assemble")

   # prepare trim and pair information
   run_process("cat %s/Assemble/out/assembly/454TrimStatus.txt |grep -v Trimpoints | grep -v left |grep -v right |awk '{print $0}' | awk '{print $1\" \"$2}' > %s/Assemble/out/454TrimNoPairs.txt"%(rundir, rundir), "Assemble")
   run_process("cat %s/Assemble/out/assembly/454TrimStatus.txt |grep left |sed s/_left//g |awk '{print $0}' | awk '{print $1\" \"$2}' > %s/Assemble/out/454TrimLeftPairs.txt"%(rundir, rundir), "Assemble")
   run_process("cat %s/Assemble/out/assembly/454TrimStatus.txt |grep right |sed s/_right//g | awk '{print $0}' | awk '{print $1\" \"$2}' > %s/Assemble/out/454TrimRightPairs.txt"%(rundir, rundir), "Assemble")

   for lib in readlibs:
       run_process("unlink %s/Preprocess/out/lib%d.seq"%(rundir, lib.id), "Assemble")
       run_process("%s/sfffile -i %s/Assemble/out/454TrimNoPairs.txt -t %s/Assemble/out/454TrimNoPairs.txt -o %s/Preprocess/out/lib%d.noPairs.sff %s/Preprocess/out/lib%d.sff"%(NEWBLER, rundir, rundir, rundir, lib.id, rundir, lib.id), "Assemble")
       run_process("%s/sffinfo -s %s/Preprocess/out/lib%d.noPairs.sff > %s/Preprocess/out/lib%d.seq"%(NEWBLER, rundir, lib.id, rundir, lib.id), "Assemble")
       run_process("%s/sfffile -i %s/Assemble/out/454TrimLeftPairs.txt -t %s/Assemble/out/454TrimLeftPairs.txt -o %s/Preprocess/out/lib%d.noPairs.sff %s/Preprocess/out/lib%d.sff"%(NEWBLER, rundir, rundir, rundir, lib.id, rundir, lib.id), "Assemble")
       run_process("%s/sffinfo -s %s/Preprocess/out/lib%d.noPairs.sff |awk '{if (match($1, \">\") == 1) { print $1\"_left\"; } else { print $0; }}' >> %s/Preprocess/out/lib%d.seq"%(NEWBLER, rundir, lib.id, rundir, lib.id), "Assemble")
       run_process("%s/sfffile -i %s/Assemble/out/454TrimRightPairs.txt -t %s/Assemble/out/454TrimRightPairs.txt -o %s/Preprocess/out/lib%d.noPairs.sff %s/Preprocess/out/lib%d.sff"%(NEWBLER, rundir, rundir, rundir, lib.id, rundir, lib.id), "Assemble")
       run_process("%s/sffinfo -s %s/Preprocess/out/lib%d.noPairs.sff |awk '{if (match($1, \">\") == 1) { print $1\"_right\"; } else { print $0; }}' >> %s/Preprocess/out/lib%d.seq"%(NEWBLER, rundir, lib.id, rundir, lib.id), "Assemble")

       run_process("cat %s/Assemble/out/454TrimLeftPairs.txt |awk '{print $1\"_left\t\"$1\"_right\"}' > %s/Preprocess/out/lib%d.seq.mates"%(rundir, rundir, lib.id), "Assemble")
       run_process("echo \"library\t%s\t%d\t%d\" >> %s/Preprocess/out/all.seq.mates"%(lib.sid, lib.mmin, lib.mmax, rundir), "Assemble")
       run_process("cat %s/Assemble/out/454TrimLeftPairs.txt |awk '{print $1\"_left\t\"$1\"_right\t%s\"}' >> %s/Preprocess/out/all.seq.mates"%(rundir, lib.sid, rundir), "Assemble")
       run_process("rm %s/Preprocess/out/lib%d.noPairs.sff"%(rundir, lib.id), "Assemble")
 
def runVelvet(velvetPath, name):
   if not os.path.exists(velvetPath + os.sep + "velvetg"):
      print "Error: %s not found in %s. Please check your path and try again.\n"%(name, velvetPath)
      raise(JobSignalledBreak)

   CATEGORIES = 0.0;
   p = subprocess.Popen("%s/velveth | grep CATEGORIES"%(velvetPath), shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   (checkStdout, checkStderr) = p.communicate()
   if checkStderr != "":
      print "Warning: Cannot determine Velvet number of supported libraries"
   else:
      mymatch = re.split('\s+=\s+', checkStdout.strip())
      if (len(mymatch) == 2 and mymatch[1] != None):
         CATEGORIES = float(mymatch[1])

   velvethCommandLine = "%s/velveth %s/Assemble/out/ %d "%(velvetPath,rundir,kmer) 
   currLibID = 1
   currLibString = "";
   for lib in readlibs:
      if (currLibID > CATEGORIES):
         print "Warning: Velvet only supports %d libraries, will not input any more libraries\n"%(CATEGORIES)
         break 

      if lib.format == "fasta":
         velvethCommandLine += "-fasta"
      elif lib.format == "fastq":
         velvethCommandLine += "-fastq"

      if lib.mated:
         velvethCommandLine += " -shortPaired%s "%(currLibString)
      else:
         velvethCommandLine += " -short%s "(currLibString)
      velvethCommandLine += "%s/Preprocess/out/lib%d.seq "%(rundir, lib.id)
      currLibID += 1
      if (currLibID > 1):
         currLibString = "%d"%(currLibID) 

   # now run velveth
   run_process("%s"%(velvethCommandLine), "Assemble")

   # now build velvetg command line
   velvetgCommandLine = "%s/velvetg %s/Assemble/out/"%(velvetPath, rundir) 

   currLibID = 1;
   currLibString = ""
   for lib in readlibs:
      if (currLibID > CATEGORIES):
         print "Warning: Velvet only supports %d libraries, will not input any more libraries\n"%(CATEGORIES)
         break

      if lib.mated:
         velvetgCommandLine += " -ins_length%s %d -ins_length%s_sd %d"%(currLibString, lib.mean, currLibString, lib.stdev)
      currLibID += 1
      if (currLibID > 1):
         currLibString = "%d"%(currLibID)
   velvetgCommandLine += " %s"%(getProgramParams("%s.spec"%(name), "", "-"))
   velvetgCommandLine += " -read_trkg yes -scaffolding no -amos_file yes";
   run_process("%s"%(velvetgCommandLine), "Assemble")

   # make symlinks
   run_process("rm %s/Assemble/out/%s.afg"%(rundir, PREFIX), "Assemble")
   run_process("ln -s %s/Assemble/out/velvet_asm.afg %s/Assemble/out/%s.afg"%(rundir, rundir, PREFIX),"Assemble")
   run_process("rm %s/Assemble/out/%s.asm.contig"%(rundir, PREFIX),"Assemble")
   run_process("ln -s %s/Assemble/out/contigs.fa %s/Assemble/out/%s.asm.contig"%(rundir, rundir, PREFIX), "Assemble")

        
def LCS(S1, S2):
    M = [[0]*(1+len(S2)) for i in xrange(1+len(S1))]
    longest, x_longest = 0, 0
    for x in xrange(1,1+len(S1)):
        for y in xrange(1,1+len(S2)):
            if S1[x-1] == S2[y-1]:
                M[x][y] = M[x-1][y-1] + 1
                if M[x][y]>longest:
                    longest = M[x][y]
                    x_longest  = x
            else:
                M[x][y] = 0
    return S1[x_longest-longest: x_longest]


def start_http(server_class=BaseHTTPServer.HTTPServer,
        handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
    #pid = os.fork()
    server_address = ('localhost', 8111)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    #return pid
def validate_run(dir):
    run_process("./%s/run.sh"%(dir))
    #check to see if all output files (listed in README) were generated
    readme = open("./%s/README"%(dir),'r')
    outf = 0
    for line in readme:
        if "[OUTPUT]" in line:
            outf = 1
        elif "[RUN]" in line:
            print "all output files successfully generated!"
            outf = 0
        if outf:
            if "." in line:
                ff = line.split(".")[-1].split(",")
                for file in ff:
                    if not os.path.exists("./%s/out/%s"%(dir,file)):
                        print "%s failed"%(dir)
                        sys.exit(1)

infile = ""

#for lib in libs:
if (format == "fastq" and mated):
    infile = f1
elif (format == "fastq" and not mated):
    infile = frg
elif (format == "fasta" and not mated):
    infile = frg
elif format == "sff":
    if frg == "":
       infile = f1
    else:
       infile = frg

#if asm == "soap":
readpaths = []
filtreadpaths = []
for lib in readlibs:
    for read in lib.reads:
        readpaths.append("%s/Preprocess/in/"%(rundir)+read.fname)
        filtreadpaths.append("%s/Preprocess/out/"%(rundir)+read.fname)
   
if "Preprocess" in forcesteps:
    for path in readpaths:
        run_process("touch %s"%path)

#@transform(readpaths,["%s/Preprocess/out/all.seq"%(rundir),"%s/Preprocess/out/all.seq.mates"%(rundir)])
@files(readpaths,"%s/Preprocess/out/preprocess.success"%(rundir))
#filtreadpaths)
def Preprocess(input,output):
   #move input files into Preprocess ./in dir
   #output will either be split fastq files in out, or AMOS bank
   if "Preprocess" in skipsteps or "preprocess" in skipsteps:
       for lib in readlibs:
           for read in lib.reads:
               run_process("ln -s -t %s/Preprocess/out/ %s/Preprocess/in/%s"%(rundir,rundir,read.fname),"Preprocess")
       return 0
   run_process("rm %s/Preprocess/out/all.seq.mates"%(rundir), "Preprocess")
   if filter == True:
       #print "filtering.."
     
       #for reads+libs
       cnt = 1
       for lib in readlibs:
           for read in lib.reads:
               if not read.filtered and read.format == "fastq" and read.mated and read.interleaved:
                   #this means we have this entire lib in one file
                   #parse out paired record (8 lines), rename header to be filename + "/1" or "/2", and remove reads with N
                   rf = open(read.path,'r')
                   npath = read.path.replace("/in/","/out/")
                   #readpath,base = os.path.split(npath)
                   #newpath = readpath+"lib%d"%(lib.id)
                   wf = open(npath,'w')
                   #wf = open(read.path.replace("/in/","/out/"),'w')
                   #wf = open(readpath+"lib%d"%(lib.id),'w')
                   start = 1
                   rcnt = 0
                   recordcnt = 0
                   record = []
                   shdr = ""
                   for line in rf.xreadlines():
                       if start:
                           s1hdr = line
                           record.append(line)
                           start = 0
                           rcnt =1

                       else:
                           if rcnt == 7:
                               #end of record
                               record.append(line)
                               rcnt +=1
                               if len(record) != 8:
                                   #something went wrong
                                   continue
                               rseq = string.upper(record[0]+record[5])                               
                               if "N" in rseq:
                                   #skip both, dont' want Ns
                                   continue
                               #update hdrs to be filename /1 or /2
                               recordcnt +=1
                               hdr = read.sid+"r"+str(recordcnt)+"/"
                               #hdr2 = lib.sid[0:3]+str((int(lib.sid[3:])+1))+str(recordcnt)+"/"
                               wf.writelines("@"+hdr+"1\n")
                               wf.writelines(record[1])
                               wf.writelines("+"+hdr+"1\n")
                               wf.writelines(record[3])
                               wf.writelines("@"+hdr+"2\n")
                               wf.writelines(record[5])
                               wf.writelines("+"+hdr+"2\n")
                               wf.writelines(record[7])
                           elif rcnt % 4 == 0:
                               s2hdr = line
                               rlcs = LCS(s1hdr,s2hdr)
                               #these should almost identical
                               if float(len(rlcs))/float(len(s1hdr)) < 0.9:
                                   #missing record somewhere, start over with this one
                                   s1hdr = line
                                   record = [line]
                                   start = 0
                                   rcnt = 1
                               else:
                                   record.append(line)
                                   rcnt +=1
                           elif rcnt % 2 == 0:
                               #quality hdr
                               record .append(line)
                               rcnt +=1
                           else:
                               record .append(line)
                               rcnt +=1
                   #update to new path
                   read.path = read.path.replace("/in/","/out/")            
                   #read.fname = "lib%d"%(lib.id)
                   read.filtered = True
               elif not read.filtered and read.format == "fastq" and read.mated and not read.interleaved:
                   readpair = lib.getPair(read.id)
                   if readpair == -1:
                       #not interleaved and mated, yet do not have 2nd file..
                       continue
                   rf1 = open(read.path,'r')
                   wf1 = open(read.path.replace("/in/","/out/"),'w')
                   rf2 = open(readpair.path,'r')
                   wf2 = open(readpair.path.replace("/in/","/out/"),'w')
                   recordcnt = 0
                   f1cnt = 0
                   f2cnt = 0
                   while 1:                   
                       rs1 = rf1.readline()
                       rs2 = rf1.readline()
                       rs3 = rf1.readline()
                       rs4 = rf1.readline()

                       rp1 = rf2.readline()
                       rp2 = rf2.readline()
                       rp3 = rf2.readline()
                       rp4 = rf2.readline()

                       if rs1 == "" or rs2 == "" or rs3 == "" or rs4 == "":
                           #EOF or something went wrong, break
                           break 
                       rseq = string.upper(rs2)                               
                       if "N" in rseq:
                           continue
                       if rp1 == "" or rp2 == "" or rp3 == "" or rp4 == "":
                           #EOF or something went wrong, break
                           break 
                       f1cnt +=4
                       f2cnt +=4
                       rseq = string.upper(rp2)                               
                       if "N" in rseq:
                           continue

                       #rlcs = LCS(rs1,rp1)
                       if 0:#float(len(rlcs))/float(len(rs1)) < 0.9:
                           #not aligned! something needs to be removed?
                           #go on to next
                           continue
                       else:
                           #record.append(line)
                           #rcnt +=1
                           recordcnt +=1
                           hdr = read.sid+"r"+str(recordcnt)+"/"
                           wf1.writelines("@"+hdr+"1\n")
                           wf1.writelines(rs2)
                           wf1.writelines("+"+hdr+"1\n")
                           wf1.writelines(rs4)
                           hdr2 = readpair.sid[0:3]+str(int(lib.sid[3:])+1)+str(recordcnt)+"/"
                           wf2.writelines("@"+hdr+"2\n")
                           wf2.writelines(rp2)
                           wf2.writelines("+"+hdr+"2\n")
                           wf2.writelines(rp4)
                           wf1.flush()
                           wf2.flush()
                   if f1cnt != f2cnt:
                       print "Error: error in library, read files not of equal length!"
                       raise(JobSignalledBreak)
                   readpair.filtered = True
                   read.filtered = True
                   read.path = read.path.replace("/in/","/out/")
                   readpair.path = readpair.path.replace("/in/","/out/")
               elif not read.filtered and read.format == "fastq" and not read.mated:
                   #this is easy, just throw out reads with Ns
                   rf = open(read.path,'r')
                   wf = open(read.path.replace("/in/","/out/"),'w')
                   while 1:
                       rs1 = rf.readline()
                       rs2 = rf.readline()
                       rs3 = rf.readline()
                       rs4 = rf.readline()
                       if rs1 == "" or rs2 == "" or rs3 == "" or rs4 == "":
                           #EOF or something went wrong, break
                           break 
                       rseq = string.upper(rs2)                               
                       if "N" in rseq:
                           continue
                       wf.writelines(rs1)
                       wf.writelines(rs2)
                       wf.writelines(rs3)
                       wf.writelines(rs4)
                   read.path = read.path.replace("/in/","/out/")
               elif not read.filtered and read.format == "fasta" and read.mated and read.interleaved:
                   #this means we have this entire lib in one file
                   #parse out paired record (4 lines), rename header to be filename + "/1" or "/2", and remove reads with N
                   rf = open(read.path,'r')
                   npath = read.path.replace("/in/","/out/")
                   #print npath
                   #readpath,base = os.path.split(npath)
                   #newpath = readpath+"lib%d"%(lib.id)
                   wf = open(npath,'w')
                   #wf = open(read.path.replace("/in/","/out/"),'w')
                   start = 1
                   rcnt = 0
                   recordcnt = 0
                   record = []
                   shdr = ""
                   reads = rf.read().split(">")[1:]
                   if len(reads) % 2 != 0:
                       print "Read file corrupted, please fix and restart!"
                       sys.exit(1)

                   prevok = False
                   first = True
                   second = False
                   prevseq = ""
                   readcnt = 1
                   for rd in reads:
                       if first:
                           hdr,seq = rd.split("\n",1)
                           if "N" in string.upper(seq) or len(seq) < 2:
                               prevok = False
                           else: 
                               prevok = True
                               prevseq = seq

                           second = True
                           first = False
                       elif second:
                           hdr,seq = rd.split("\n",1)
                           if "N" in string.upper(seq) or len(seq) < 2:
                               pass
                           elif prevok:
                               hdr = read.sid+"r"+str(readcnt)+"/"
                               wf.writelines(">"+hdr+"1\n")
                               wf.writelines(prevseq)
                               wf.writelines(">"+hdr+"2\n")
                               wf.writelines(seq)
                               readcnt +=1
                           second = False
                           first = True

                   #update to new path
                   read.path = read.path.replace("/in/","/out/")            

                   #read.path = newpath#read.path.replace("/in/","/out/")            
                   #read.fname = "lib%d"%(lib.id)
               elif not read.filtered and read.format == "fasta" and read.mated and not read.interleaved:
                   readpair = lib.getPair(read.id)
                   if readpair == -1:
                       #not interleaved and mated, yet do not have 2nd file..
                       continue
                   rf1 = open(read.path,'r')
                   wf1 = open(read.path.replace("/in/","/out/"),'w')
                   rf2 = open(readpair.path,'r')
                   wf2 = open(readpair.path.replace("/in/","/out/"),'w')
                   recordcnt = 0
                   while 1:                   
                       rs1 = rf1.readline()
                       rs2 = rf1.readline()

                       if rs1 == "" or rs2 == "":
                           #EOF or something went wrong, break
                           break 
                       rseq = string.upper(rs2)                               
                       if "N" in rseq:
                           continue
                       rp1 = rf2.readline()
                       rp2 = rf2.readline()

                       if rp1 == "" or rp2 == "":
                           #EOF or something went wrong, break
                           break 
                       rseq = string.upper(rp2)                               
                       if "N" in rseq:
                           continue

                       rlcs = LCS(rs1,rp1)
                       if 0:#float(len(rlcs))/float(len(rs1)) < 0.9:
                           #not aligned! something needs to be removed?
                           #go on to next
                           continue
                       else:
                           #record.append(line)
                           #rcnt +=1
                           recordcnt +=1
                           hdr = read.sid+"r"+str(recordcnt)+"/"
                           wf1.writelines(">"+hdr+"1\n")
                           wf1.writelines(rs2)
                           wf2.writelines(">"+hdr+"2\n")
                           wf2.writelines(rp2)

                   readpair.filtered = True
                   read.filtered = True
                   read.path = read.path.replace("/in/","/out/")
                   readpair.path = readpair.path.replace("/in/","/out/")
               elif not read.filtered and read.format == "fasta" and not read.mated:
                   #easiest case, check for Ns
                   rf = open(read.path,'r')
                   wf = open(read.path.replace("/in/","/out/"),'w')
                   while 1:
                       rs1 = rf.readline()
                       rs2 = rf.readline()
                       if rs1 == "" or rs2 == "":
                           #EOF or something went wrong, break
                           break
                       rseq = string.upper(rs2)                               
                       if "N" in rseq:
                           continue
                       wf.writelines(rs1)
                       wf.writelines(rs2)
                   read.path = read.path.replace("/in/","/out/")
           cnt +=1
   else:
       for lib in readlibs:
           for read in lib.reads:
               run_process("ln -s -t %s/Preprocess/out/ %s/Preprocess/in/%s"%(rundir,rundir,read.fname),"Preprocess")
   #PUNT HERE
   for lib in readlibs:
      if 1:
           #this means interleaved, single file
           if lib.format == "sff":
               run_process("unlink %s/Preprocess/out/lib%d.sff"%(rundir, lib.id), "Preprocess")
               run_process("ln -s %s %s/Preprocess/out/lib%d.sff"%(read.path, rundir, lib.id), "Preprocess")

               if asm == "newbler":
                  run_process("touch %s/Preprocess/out/lib%d.seq"%(rundir, lib.id), "Preprocess");
               else:
                  if not os.path.exists(CA + os.sep + "sffToCA"):
                     print "Error: CA not found in %s. It is needed to convert SFF files to fasta.\n"%(CA)
                     raise(JobSignalledBreak)

                  # generate the fasta files from the sff file
                  run_process("rm -rf %s/Preprocess/out/%s.tmpStore"%(rundir, PREFIX), "Preprocess")
                  run_process("rm -rf %s/Preprocess/out/%s.gkpStore"%(rundir, PREFIX), "Preprocess")
                  run_process("unlink %s/Preprocess/out/%s.frg"%(rundir, PREFIX), "Preprocess")
                  sffToCACmd = "%s/sffToCA -clear discard-n "%(CA)
                  if lib.linkerType != "flx":
                     sffToCACmd += "-clear 454 "
                  sffToCACmd += "-trim hard -libraryname lib%d -output %s/Preprocess/out/lib%d"%(lib.id, rundir, lib.id)
                  if (read.mated == True):
                      run_process("%s -linker %s -insertsize %d %d %s"%(sffToCACmd, lib.linkerType, lib.mean, lib.stdev, read.path),"Preprocess")
                  else:
                      run_process("%s %s"%(sffToCACmd, read.path),"Preprocess")
                  run_process("%s/gatekeeper -T -F -o %s/Preprocess/out/%s.gkpStore %s/Preprocess/out/lib%d.frg"%(CA, rundir, PREFIX, rundir, lib.id),"Preprocess")
                  run_process("%s/gatekeeper -dumpnewbler %s/Preprocess/out/lib%d %s/Preprocess/out/%s.gkpStore"%(CA, rundir, lib.id, rundir, PREFIX),"Preprocess")
                  run_process("%s/gatekeeper -dumpfastq   %s/Preprocess/out/lib%d %s/Preprocess/out/%s.gkpStore"%(CA, rundir, lib.id, rundir, PREFIX), "Preprocess")
                  run_process("%s/gatekeeper -dumplibraries -tabular %s/Preprocess/out/%s.gkpStore |awk '{if (match($3, \"U\") == 0 && match($1, \"UID\") == 0) print \"library\t\"$1\"\t\"$4-$5*3\"\t\"$4+$5*3}' >> %s/Preprocess/out/all.seq.mates"%(CA, rundir, PREFIX, rundir),"Preprocess")
                  run_process("%s/gatekeeper -dumpfragments -tabular %s/Preprocess/out/%s.gkpStore|awk '{if ($3 != 0 && match($1, \"UID\")==0 && $1 < $3) print $1\"\t\"$3\"\t\"$5}' >> %s/Preprocess/out/all.seq.mates"%(CA, rundir, PREFIX, rundir),"Preprocess")
                  run_process("%s/gatekeeper -dumpfragments -tabular %s/Preprocess/out/%s.gkpStore|awk '{if ($3 != 0 && match($1, \"UID\")==0 && $1 < $3) print $1\"\t\"$3}' > %s/Preprocess/out/lib%d.seq.mates"%(CA, rundir, PREFIX, rundir, lib.id), "Preprocess")
                  run_process("unlink %s/Preprocess/out/lib%d.seq"%(rundir,lib.id),"Preprocess")
                  run_process("ln -s %s/Preprocess/out/lib%d.fna %s/Preprocess/out/lib%d.seq"%(rundir,lib.id,rundir,lib.id),"Preprocess")
                  run_process("ln -s %s/Preprocess/out/lib%d.fna.qual %s/Preprocess/out/lib%d.seq.qual"%(rundir,lib.id,rundir,lib.id),"Preprocess")
                  run_process("rm -rf %s/Preproces/out/%s.gkpStore"%(rundir, PREFIX),"Preprocess")
                  run_process("cat %s/Preprocess/out/lib%d.seq.mates >> %s/Preprocess/out/all.seq.mates"%(rundir, lib.id, rundir), "Preprocess")

                  if asm != "CA":
                     #flip the type to fastq
                     lib.format = "fastq"
                     lib.interleaved = False
                     if lib.mated:
                        lib.f1 = Read(lib.format,"%s/Preprocess/out/lib%d.1.fastq"%(rundir, lib.id),lib.mated,lib.interleaved) 
                        lib.f2 = Read(lib.format,"%s/Preprocess/out/lib%d.2.fastq"%(rundir, lib.id),lib.mated,lib.interleaved) 
                     else:
                        lib.f1 = Read(lib.format,"%s/Preprocess/out/lib%d.unmated.fastq"%(rundir, lib.id),lib.mated,lib.interleaved)  
           elif lib.format == "fasta" and not lib.mated:
               run_process("ln -s %s/Preprocess/in/%s %s/Preprocess/out/lib%d.seq"%(rundir,lib.f1.fname,rundir,lib.id),"Preprocess")
               run_process("ln -s %s/Preprocess/in/%s.qual %s/Preprocess/out/lib%d.seq.qual"%(rundir,lib.f1.fname,rundir,lib.id),"Preprocess")
               run_process("touch %s/Preprocess/out/lib%d.seq.mates"%(rundir,lib.id),"Preprocess")
           elif lib.format == "fastq" and not lib.mated:
               run_process("ln -s %s/Preprocess/in/%s %s/Preprocess/out/lib%d.seq"%(rundir, lib.fq, fname, rundir, lib.id), "Preprocess")
               run_process("touch %s/Preprocess/out/lib%d.seq.mates"%(rundir, lib.id), "Preprocess")
           elif format == "fasta" and mated and not interleaved:
               #FIXME, make me faster!
               run_process("perl %s/perl/shuffleSequences_fasta.pl  %s/Preprocess/out/%s %s/Preprocess/out/%s %s/Preprocess/out/lib%d.seq"%(METAMOS_UTILS,rundir,lib.f1.fname, rundir,lib.f2.fname,rundir,lib.id),"Preprocess")
               run_process("python %s/python/extract_mates_from_fasta.py %s/Preprocess/out/lib%d.seq"%(METAMOS_UTILS,rundir,lib.id),"Preprocess")
               run_process("unlink %s/Preprocess/out/lib%d.seq.mates"%(rundir, lib.id),"Preprocess")
               run_process("ln -t %s/Preprocess/out/ -s %s/Preprocess/in/lib%d.seq.mates"%(rundir,rundir,lib.id),"Preprocess")
           elif format == "fastq" and mated and not interleaved:
               #extract mates from fastq
               run_process("perl %s/perl/shuffleSequences_fastq.pl  %s/Preprocess/out/%s %s/Preprocess/out/%s %s/Preprocess/out/lib%d.seq"%(METAMOS_UTILS,rundir,lib.f1.fname, rundir,lib.f2.fname,rundir,lib.id),"Preprocess")
               run_process("python %s/python/extract_mates_from_fastq.py %s/Preprocess/out/lib%d.seq"%(METAMOS_UTILS,rundir,lib.id),"Preprocess")
           elif mated and interleaved:
               run_process("cp %s/Preprocess/out/%s %s/Preprocess/out/lib%d.seq"%(rundir,lib.f1.fname,rundir,lib.id),"Preprocess")
               if format == "fastq":
                   run_process("python %s/python/extract_mates_from_fastq.py %s/Preprocess/out/lib%d.seq"%(METAMOS_UTILS,rundir,lib.id),"Preprocess")
               else:
                   run_process("python %s/python/extract_mates_from_fasta.py %s/Preprocess/out/lib%d.seq"%(METAMOS_UTILS,rundir,lib.id),"Preprocess")
           #update_soap_config()
           elif asm == "ca":
               #useful for 454, need to get SFF to FRG?
               #/fs/wrenhomes/sergek/wgs-assembler/Linux-amd64/bin/sffToCA
               pass
           elif asm == "amos":
               #call toAmos_new              
               pass
   run_process("touch %s/Preprocess/out/preprocess.success"%(rundir),"Preprocess")

asmfiles = []
#if asm == "soap"

for lib in readlibs:
    #print "touch"
    if "Assemble" in forcesteps:
        #print lib.id
        run_process("touch %s/Preprocess/out/lib%d.seq"%(rundir,lib.id))

    asmfiles.append("%s/Preprocess/out/lib%d.seq"%(rundir,lib.id))

if "Assemble" not in skipsteps and "Assemble" in forcesteps:
    run_process("rm %s/Assemble/out/%s.asm.contig"%(rundir,PREFIX))
@files(asmfiles,["%s/Assemble/out/%s.asm.contig"%(rundir,PREFIX)])
#@posttask(create_symlink,touch_file("completed.flag"))
@follows(Preprocess)
def Assemble(input,output):
   #pick assembler
   if "Assemble" in skipsteps or "assemble" in skipsteps:
      return 0
   if asm == "soap":
      #open & update config
      soapf = open("%s/config.txt"%(rundir),'r')
      soapd = soapf.read()
      soapf.close()
      cnt = 1
      libno = 1
      #print libs
      for lib in readlibs:
          if (lib.format == "fastq" or lib.format == "fasta")  and lib.mated and not lib.interleaved:
              soapd = soapd.replace("LIB%dQ1REPLACE"%(lib.id),"%s/Preprocess/out/%s"%(rundir,lib.f1.fname))
              soapd = soapd.replace("LIB%dQ2REPLACE"%(lib.id),"%s/Preprocess/out/%s"%(rundir,lib.f2.fname))

          elif lib.format == "fastq"  and lib.mated and lib.interleaved:
              #this is NOT supported by SOAP, make sure files are split into two..
              #need to update lib.f2 path
              run_process("perl spilt_fastq.pl %s/Preprocess/out/%s %s/Preprocess/out/%s %s/Preprocess/out/%s"%(lib.f1.fname,lib.f1.fname,lib.f2.fname),"Assemble")
              soapd = soapd.replace("LIB%dQ1REPLACE"%(lib.id),"%s/Preprocess/out/%s"%(rundir,lib.f1.fname))
              soapd = soapd.replace("LIB%dQ2REPLACE"%(lib.id),"%s/Preprocess/out/%s"%(rundir,lib.f2.fname))

          elif format == "fasta"  and mated and interleaved:
              soapd = soapd.replace("LIB%dQ1REPLACE"%(lib.id),"%s/Preprocess/out/%s"%(rundir,lib.f1.fname))
          else:
              soapd = soapd.replace("LIB%dQ1REPLACE"%(lib.id),"%s/Preprocess/out/%s"%(rundir,lib.f1.fname))

      #cnt +=1
      soapw = open("%s/soapconfig.txt"%(rundir),'w')
      soapw.write(soapd)
      soapw.close()

      if not os.path.exists(SOAP + os.sep + "soap63"):
         print "Error: SOAPdenovo not found in %s. Please check your path and try again.\n"%(SOAP)
         raise(JobSignalledBreak)

      print "Running SOAPdenovo on input reads..."
      soapOptions = getProgramParams("soap.spec", "", "-") 
      #start stopwatch
      run_process("%s/soap63 all -p %d -K %d %s -s %s/soapconfig.txt -o %s/Assemble/out/%s.asm"%(SOAP, threads, kmer, soapOptions, rundir,rundir,PREFIX),"Assemble")#SOAPdenovo config.txt

      #if OK, convert output to AMOS
   elif asm == "metaidba":
      bowtie_mapping = 1
      for lib in readlibs:
          if lib.format != "fasta"  or (lib.mated and not lib.interleaved):
              print "ERROR: meta-IDBA requires reads to be in (interleaved) fasta format, cannot run"
              sys.exit(1)
          #apparently connect = scaffold? need to convert fastq to interleaved fasta to run, one lib per run??
          #print "%s/metaidba --read %s/Preprocess/out/%s --output  %s/Assemble/out/%s.asm --mink 21 --maxk %d --cover 1 --connect"%(METAIDBA,rundir,lib.f1.fname,rundir,PREFIX,kmer)
          run_process("%s/metaidba --read %s/Preprocess/out/%s --output  %s/Assemble/out/%s.asm --mink 21 --maxk %d --cover 1 --connect"%(METAIDBA,rundir,lib.f1.fname,rundir,PREFIX,kmer),"Assemble")
          run_process("mv %s/Assemble/out/%s.asm-contig.fa %s/Assemble/out/%s.asm.contig"%(rundir,PREFIX,rundir,PREFIX),"Assemble")

   elif asm == "newbler":
      if not os.path.exists(NEWBLER + os.sep + "newAssembly"):
         print "Error: Newbler not found in %s. Please check your path and try again.\n"%(NEWBLER)
         raise(JobSignalledBreak)

      run_process("%s/newAssembly -force %s/Assemble/out"%(NEWBLER, rundir),"Assemble")

      NEWBLER_VERSION = 0.0;
      p = subprocess.Popen("%s/newAssembly --version | head -n 1"%(NEWBLER), shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
      (checkStdout, checkStderr) = p.communicate()
      if checkStderr != "":
         print "Warning: Cannot determine Newbler version"
      else:
         mymatch = re.findall('\d+\.\d+', checkStdout.strip())
         if (len(mymatch) == 1 and mymatch[0] != None):
            NEWBLER_VERSION = float(mymatch[0])

      for lib in readlibs:
          if lib.format == "fasta":
              run_process("%s/addRun %s/Assemble/out %s/Preprocess/out/lib%d.seq"%(NEWBLER, rundir, rundir,lib.id),"Assemble")
          elif lib.format == "sff":
              run_process("%s/addRun %s %s/Assemble/out %s/Preprocess/out/lib%d.sff"%(NEWBLER, ("-p" if lib.mated else ""), rundir, rundir, lib.id), "Assemble")
          elif lib.format == "fastq" and lib.interleaved:
              if (NEWBLER_VERSION < 2.6):
                 print "Error: FASTQ + Newbler only supported in Newbler version 2.6+. You are using version %s."%(NEWBLER_VERSION)
                 raise(JobSignalledBreak)
              run_process("%s/addRun %s/Assemble/out %s/Preprocess/out/lib%d.seq"%(NEWBLER, rundir, rundir, lib.id),"Assemble")
          elif not lib.interleaved:
              print "Error: Only interleaved fastq files are supported for Newbler"
              raise(JobSignalledBreak)

      newblerCmd = "%s%srunProject "%(NEWBLER, os.sep)
      # read spec file to input to newbler parameters
      newblerCmd += getProgramParams("newbler.spec", "", "-")
      run_process("%s -cpu %d %s/Assemble/out"%(newblerCmd,threads,rundir),"Assemble")

      # unlike other assemblers, we can only get the preprocess info for newbler after assembly (since it has to split sff files by mates)
      extractNewblerReads()

      # convert to AMOS
      run_process("cat %s/Assemble/out/assembly/454Contigs.ace |awk '{if (match($2, \"\\\\.\")) {STR= $1\" \"substr($2, 1, index($2, \".\")-1); for (i = 3; i <=NF; i++) STR= STR\" \"$i; print STR} else { print $0} }' > %s/Assemble/out/%s.ace"%(rundir, rundir,PREFIX), "Assemble") 
      run_process("%s/toAmos -o %s/Assemble/out/%s.mates.afg -m %s/Preprocess/out/all.seq.mates -ace %s/Assemble/out/%s.ace"%(AMOS,rundir, PREFIX, rundir, rundir, PREFIX),"Assemble")
      # get info on EID/IIDs for contigs
      run_process("cat %s/Assemble/out/%s.mates.afg | grep -A 3 \"{CTG\" |awk '{if (match($1, \"iid\") != 0) {IID = $1} else if (match($1, \"eid\") != 0) {print $1\" \"IID; } }'|sed s/eid://g |sed s/iid://g > %s/Assemble/out/454eidToIID"%(rundir, PREFIX, rundir),"Assemble")
      run_process("java -cp %s convert454GraphToCTL %s/Assemble/out/454eidToIID %s/Assemble/out/assembly/454ContigGraph.txt > %s/Assemble/out/%s.graph.cte"%(METAMOS_JAVA, rundir, rundir, rundir, PREFIX),"Assemble")
      run_process("cat %s/Assemble/out/%s.mates.afg %s/Assemble/out/%s.graph.cte > %s/Assemble/out/%s.afg"%(rundir, PREFIX, rundir, PREFIX, rundir, PREFIX),"Assemble")
    
      # make symlink for subsequent steps
      run_process("rm %s/Assemble/out/%s.asm.contig"%(rundir, PREFIX),"Assemble")
      run_process("ln -s %s/Assemble/out/assembly/454AllContigs.fna %s/Assemble/out/%s.asm.contig"%(rundir, rundir, PREFIX),"Assemble")
      if mated == True:
         run_process("ln -s %s/Assemble/out/assembly/454Scaffolds.fna %s/Assemble/out/%s.asm.scafSeq"%(rundir, rundir, PREFIX),"Assemble")
      else:
         run_process("ln -s %s/Assemble/out/assembly/454AllContigs.fna %s/Assemble/out/%s.asm.scafSeq"%(rundir, rundir, PREFIX),"Assemble")

   elif asm == "amos":
      run_process("%s/Minimus %s/Preprocess/out/bank"%(AMOS,rundir),"Assemble")
   elif asm == "CA" or asm == "ca":
      #runCA script
      frglist = ""
      matedString = ""
      for lib in readlibs:
          for read in lib.reads:
              if read.format == "fastq":
                  if lib.mated:
                      matedString = "-insertsize %d %d -%s"%(lib.mean, lib.stdev, "innie" if lib.innie else "outtie") 
                  run_process("%s/fastqToCA %s -libraryname %s -t illumina -fastq %s/Preprocess/in/%s > %/Preprocess/out/lib%d.frg"%(CA, matedString, lib.read.path, rundir, PREFIX, rundir, lib.id),"Assemble")
              elif read.format == "fasta":
                  if lib.mated:
                      matedString = "-mean %d -stddev %d -m %s/Preprocess/out/lib%d.seq.mates"%(lib.mean, lib.stdev, lib.id)
                  run_process("%s/convert-fasta-to-v2.pl -l %s %s -s %s/Preprocess/in/%s -q %s/Preprocess/in/%s.qual > %s/Preprocess/out/lib%d.frg"%(CA, lib.sid, matedString, rundir, read.fname, rundir, read.fname, rundir, read.fname,rundir),"Assemble")
              frglist += "%s/Preprocess/out/lib%d.frg"%(rundir, lib.id)
      run_process("%s/runCA -p %s -d %s/Assemble/out/ -s %s/config/asm.spec %s"%(CA,PREFIX,rundir,METAMOS_UTILS,frglist),"Assemble")
      #convert CA to AMOS
      run_process("%s/gatekeeper -dumpfrg -allreads %s.gkpStore > %s.frg"%(CA, PREFIX, PREFIX),"Assemble")
      run_process("%s/terminator -g %s.gkpStore -t %s.tigStore/ 2 -o %s"%(CA, PREFIX, PREFIX, PREFIX),"Assemble")
      run_process("%s/asmOutputFasta -p %s < %s.asm"%(CA, PREFIX, PREFIX), "Assemble")
      run_process("ln -s %s.utg.fasta %s.asm.contig"%(PREFIX, PREFIX), "Assemble")
   elif asm == "velvet":
      runVelvet(VELVET, "velvet")
   elif asm == "velvet-sc":
      runVelvet(VELVET_SC, "velvet-sc")
   elif asm == "none":
      pass
   else:  
       print "Error: %s is an unknown assembler. No valid assembler specified."%(asm)
      raise(JobSignalledBreak)

   if 1:
       if "bowtie" not in skipsteps:
           map2contig()
   #stop here, for now
   #sys.exit(0)
   #check if sucessfully completed   

if "FindORFS" in forcesteps:
   run_process("rm %s/FindORFS/out/%s.faa"%(rundir,PREFIX))
@follows(Assemble)
@files("%s/Assemble/out/%s.asm.contig"%(rundir,PREFIX),"%s/FindORFS/out/%s.faa"%(rundir,PREFIX))
def FindORFS(input,output):
   if "FindORFS" in skipsteps:
      run_process("touch %s/FindRepeats/in/%s.fna"%(rundir, PREFIX),"FindORFS")
      run_process("touch %s/FindORFS/out/%s.faa"%(rundir, PREFIX),"FindORFS")
      return 0

   if asm == "soap":
         
       #if not os.path.exists("%s/Assemble/out/%s.asm.scafSeq.contigs"%(rundir,PREFIX)):
       #    run_process("python %s/python/extract_soap_contigs.py %s/Assemble/out/%s.asm.scafSeq"%(METAMOS_UTILS,rundir,PREFIX))
       #run_process("unlink %s/FindORFS/in/%s.asm.scafSeq.contigs"%(rundir,PREFIX))
       #run_process("unlink %s/FindORFS/in/%s.asm.contig"%(rundir,PREFIX))
       #run_process("ln -t %s/FindORFS/in/ -s %s/Assemble/out/%s.asm.scafSeq.contigs"%(rundir, rundir,PREFIX))
       #run_process("cp %s/FindORFS/in/%s.asm.scafSeq.contigs  %s/FindORFS/in/%s.asm.contig"%(rundir,PREFIX,rundir,PREFIX))
       #try using contigs instead of contigs extracted from scaffolds
       run_process("cp %s/Assemble/out/%s.asm.contig  %s/FindORFS/in/%s.asm.contig"%(rundir,PREFIX,rundir,PREFIX),"FindORFS")
   else:

       run_process("unlink %s/FindORFS/in/%s.asm.contig"%(rundir,PREFIX),"FindORFS")
       run_process("ln -t %s/FindORFS/in/ -s %s/Assemble/out/%s.asm.contig"%(rundir,rundir,PREFIX),"FindORFS")


   #run_process("ln -t %s/FindORFS/in/ -s %s/Assemble/out/%s.asm.scafSeq.contigs"%(rundir,rundir,PREFIX))
   run_process("%s/gmhmmp -o %s/FindORFS/out/%s.orfs -m %s/config/MetaGeneMark_v1.mod -d -a %s/FindORFS/in/%s.asm.contig"%(GMHMMP,rundir,PREFIX,METAMOS_UTILS,rundir,PREFIX),"FindORFS")
   parse_genemarkout("%s/FindORFS/out/%s.orfs"%(rundir,PREFIX))
   run_process("unlink %s/Annotate/in/%s.faa"%(rundir,PREFIX),"FindORFS")
   run_process("unlink %s/Annotate/in/%s.fna"%(rundir,PREFIX),"FindORFS")
   run_process("unlink %s/FindRepeats/in/%s.fna"%(rundir,PREFIX),"FindORFS")
   run_process("ln -t %s/Annotate/in/ -s %s/FindORFS/out/%s.faa"%(rundir,rundir,PREFIX),"FindORFS")
   run_process("ln -t %s/FindRepeats/in/ -s %s/FindORFS/out/%s.fna"%(rundir,rundir,PREFIX),"FindORFS")

@follows(FindORFS)
@files("%s/FindRepeats/in/%s.fna"%(rundir,PREFIX),"%s/FindRepeats/out/%s.repeats"%(rundir,PREFIX))
def FindRepeats(input,output):
   if "FindORFS" in skipsteps or "FindRepeats" in skipsteps:
     return 0

   #run_process("python %s/python/getContigRepeats.py %s/FindRepeats/in/%s.fna %s/FindRepeats/out/%s.repeats"%(METAMOS_UTILS,rundir,PREFIX,rundir,PREFIX),"Findrepeats")
   getContigRepeats("%s/FindRepeats/in/%s.fna"%(rundir,PREFIX), "%s/FindRepeats/out/%s.repeats"%(rundir,PREFIX))

if "Annotate" in forcesteps:
   run_process("rm %s/Annotate/out/%s.hits"%(rundir,PREFIX))
@follows(FindRepeats)
@files("%s/Annotate/in/%s.faa"%(rundir,PREFIX),"%s/Annotate/out/%s.hits"%(rundir,PREFIX))
def Annotate(input,output):
   if "Annotate" in skipsteps or "FindORFS" in skipsteps:
      run_process("touch %s/Annotate/out/%s.hits"%(rundir, PREFIX), "Annotate")
      return 0

   #annotate contigs > 1000bp with FCP
   #lets start by annotating ORFs with phmmer
   if cls == "phmmer":
       if not os.path.exists(PHMMER + os.sep + "phmmer"):
          print "Error: PHMMER not found in %s. Please check your path and try again.\n"%(PHMMER)
          raise(JobSignalledBreak)

       if not os.path.exists("%s/DB/allprots.faa"%(METAMOS_UTILS)):
          print "Error: You indicated you would like to run phmmer but DB allprots.faa not found in %s/DB. Please check your path and try again.\n"%(METAMOS_UTILS)
          raise(JobSignalledBreak)

       run_process("%s/phmmer --cpu %d -E 0.0000000000000001 -o %s/Annotate/out/%s.phm.out --tblout %s/Annotate/out/%s.phm.tbl --notextw %s/Annotate/in/%s.faa %s/DB/allprots.faa"%(PHMMER, threads,rundir,PREFIX,rundir,PREFIX,rundir,PREFIX,METAMOS_UTILS),"Annotate")
       parse_phmmerout("%s/Annotate/out/%s.phm.tbl"%(rundir,PREFIX))
       run_process("cp %s/Annotate/out/%s.phm.tbl  %s/Postprocess/in/%s.hits"%(rundir,PREFIX,rundir,PREFIX),"Annotate")
       run_process("mv %s/Annotate/out/%s.phm.tbl  %s/Annotate/out/%s.hits"%(rundir,PREFIX,rundir,PREFIX),"Annotate")
       #run_process("mv %s/Annotate/out/%s.phm.tbl  %s/Annotate/out/%s.annotate"%(rundir,PREFIX,rundir,PREFIX))
   elif cls == "blast":
       if not os.path.exists(BLAST + os.sep + "blastall"):
          print "Error: BLAST not found in %s. Please check your path and try again.\n"%(BLAST)
          raise(JobSignalledBreak)

       if not os.path.exists("%s/DB/allprots.faa"%(METAMOS_UTILS)):
          print "Error: You indicated you would like to run BLAST but DB allprots.faa not found in %s/DB. Please check your path and try again.\n"%(METAMOS_UTILS)
          raise(JobSignalledBreak)
       run_process("%s/blastall -v 1 -b 1 -a %d -p blastp -m 8 -e 0.00001 -i %s/Annotate/in/%s.faa -d %s/DB/refseq_protein -o %s/Annotate/out/%s.blastout"%(BLAST, threads, rundir,PREFIX,METAMOS_UTILS,rundir,PREFIX),"Annotate")
       run_process("cp %s/Annotate/out/%s.blastout  %s/Postprocess/in/%s.hits"%(rundir,PREFIX,rundir,PREFIX),"Annotate")
       run_process("mv %s/Annotate/out/%s.blastout  %s/Annotate/out/%s.hits"%(rundir,PREFIX,rundir,PREFIX),"Annotate")
   elif cls == "amphora":
       if AMPHORA == "" or not os.path.exists(AMPHORA + os.sep + "amphora2"):
          print "Error: AMPHORA not found in %s. Please check your path and try again.\n"%(AMPHORA)
          raise(JobSignalledBreak)

       run_process("unlink %s/Annotate/in/%s.asm.contig"%(rundir, PREFIX), "Annotate")
       run_process("ln -t %s/Annotate/in/ -s %s/Assemble/out/%s.asm.contig"%(rundir, rundir, PREFIX), "Annotate")

       amphoraCmd =  "%s/amphora2 all --threaded=%d"%(AMPHORA, threads)
       amphoraCmd += " %s"%(getProgramParams("amphora.spec", "", "--"))
       # run on contigs for now
       #for lib in readlibs:
       #   if lib.mated:
       #       if not lib.innie or lib.interleaved:
       #          print "Warning: Amphora only supports innie non-interleaved libraries now, skipping library %d"%(lib.id)
       #       else:
       #          run_process("%s -paired %s/Preprocess/in/%s %s/Preprocess/in/%s"%(amphoraCmd,rundir,lib.f1.fname,rundir,lib.f2.fname), "Annotate")
       #   else:
       #      run_process("%s %s/Preprocess/out/lib%d.seq"%(amphoraCmd,rundir,lib.id), "Annotate")
       run_process("%s %s/Annotate/in/%s.asm.contig --coverage=%s/Assemble/out/%s.contig.cvg "%(amphoraCmd, rundir, PREFIX,rundir,PREFIX), "Annotate")

       # save the results
       run_process("unlink %s/Annotate/out/%s.hits"%(rundir, PREFIX), "Annotate")
       run_process("ln -s %s/Annotate/out/Amph_temp/%s.asm.contig/sequence_taxa_summary.txt %s/Annotate/out/%s.hits"%(rundir, PREFIX, rundir, PREFIX), "Annotate") 
       run_process("unlink %s/Postprocess/in/%s.hits"%(rundir, PREFIX), "Annotate")
       run_process("unlink %s/Postprocess/out/%s.hits"%(rundir, PREFIX), "Annotate")
       run_process("ln -s %s/Annotate/out/%s.hits %s/Postprocess/in/%s.hits"%(rundir, PREFIX, rundir, PREFIX), "Annotate")
       run_process("cp %s/Annotate/out/%s.hits %s/Postprocess/out/%s.hits"%(rundir, PREFIX, rundir, PREFIX), "Annotate")
       
       if not os.path.exists(KRONA + os.sep + "ImportAmphora.pl"):
           print "Error: Krona importer for Amphora 2 not found in %s. Please check your path and try again.\n"%(KRONA)
           raise(JobSignalledBreak)
       run_process("perl %s/ImportAmphora.pl -c -v -i %s/Annotate/out/%s.hits:%s/Assemble/out/%s.contig.cvg"%(KRONA,rundir,PREFIX,rundir,PREFIX), "Annotate")

   elif cls == "fcp":
       print "FCP not yet supported.. stay tuned"
   elif cls == "phymm":
       print "Phymm not yet supported.. stay tuned"
   elif cls == None:
       print "No method specified, skipping"

if "Abundance" in forcesteps:
   run_process("touch %s/FindORFS/out/%s.faa"%(rundir,PREFIX))
   run_process("rm %s/Abundance/out/%s.taxprof.pct.txt"%(rundir,PREFIX))

@follows(FindORFS)
@files("%s/Assemble/out/%s.asm.contig"%(rundir,PREFIX),"%s/Abundance/out/%s.taxprof.pct.txt"%(rundir,PREFIX))
def Abundance(input,output):
   if "FindORFS" in skipsteps or "Abundance" in skipsteps:
      return 0

   #run_process("unlink %s/Abundance/in/%s.gene.cvg"%(rundir,PREFIX),"Abundance")
   #run_process("unlink %s/Abundance/in/%s.faa"%(rundir,PREFIX),"Abundance")
   #run_process("ln -t %s/Abundance/in/ -s %s/FindORFS/out/%s.faa"%(rundir,rundir,PREFIX),"Abundance")
   #run_process("ln -t %s/Abundance/in/ -s %s/FindORFS/out/%s.gene.cvg"%(rundir,rundir,PREFIX),"Abundance")
   blastfile = PREFIX+".blastx"
   blastc = BLAST + os.sep + "blastall"
   formatc = BLAST + os.sep + "formatdb"
   run_process("%s  -p T -i %s/DB/markers.pfasta"%(formatc,METAMOS_UTILS),"Abundance")
   run_process("%s -p blastp -i %s/FindORFS/out/%s.faa -d %s/DB/markers.pfasta -m8 -b10 -v10 -a %s -o %s/Abundance/out/%s.blastp"%(blastc, rundir,PREFIX,METAMOS_UTILS,threads,rundir,PREFIX),"Abundance")

   run_process("perl %s/perl/metaphyler_contigs.pl %s/Abundance/out/%s.blastp %s %s/FindORFS/out/%s.gene.cvg %s/Abundance/out %s"%(METAMOS_UTILS,rundir,PREFIX,PREFIX,rundir,PREFIX,rundir,METAMOS_UTILS),"Abundance")

   # finally add the GI numbers to the results where we can
   parse_metaphyler("%s/DB/markers.toGI.txt"%(METAMOS_UTILS), "%s/Abundance/out/%s.blastp"%(rundir, PREFIX), "%s/Abundance/out/%s.gi.blastp"%(rundir, PREFIX))
   run_process("cp %s/Abundance/out/%s.gi.blastp %s/Postprocess/in/%s.hits"%(rundir, PREFIX,rundir,PREFIX))

   
if "Scaffold" in forcesteps:
    #run_process("touch %s/Assemble/out/%s.asm.contig"%(rundir,PREFIX))
    run_process("rm %s/Scaffold/out/%s.scaffolds.final"%(rundir,PREFIX))
@follows(FindRepeats)
@files(["%s/Assemble/out/%s.asm.contig"%(rundir,PREFIX)],"%s/Scaffold/out/%s.scaffolds.final"%(rundir,PREFIX))
def Scaffold(input,output):
   # check if we need to do scaffolding
   numMates = 0
   if not retainBank:
       run_process("rm -rf %s/Scaffold/in/%s.bnk"%(rundir,PREFIX),"Scaffold")
       if asm == "newbler":
          p = subprocess.Popen("cat %s/Assemble/out/%s.graph.cte |grep \"{CTL\" |wc -l"%(rundir, PREFIX), stdin=None, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          (checkStdout, checkStderr) = p.communicate()
          numMates = int(checkStdout.strip())

       if mated == False and numMates == 0:

          print "No mate pair info available for scaffolding, skipping"
          run_process("touch %s/Scaffold/out/%s.linearize.scaffolds.final"%(rundir, PREFIX), "Scaffold")
          skipsteps.append("FindScaffoldORFS")
          return 0

       if asm == "soap":
           for lib in readlibs:
        
               if lib.format == "fasta":
                   run_process("%s/toAmos_new -s %s/Preprocess/out/lib%d.seq -m %s/Assemble/out/%s.lib%d.mappedmates -b %s/Scaffold/in/%s.bnk "%(AMOS,rundir,lib.id,rundir, PREFIX,lib.id,rundir,PREFIX),"Scaffold")

               elif format == "fastq":
                   run_process("%s/toAmos_new -Q %s/Preprocess/out/lib%d.seq -m %s/Assemble/out/%s.lib%d.mappedmates -b %s/Scaffold/in/%s.bnk "%(AMOS,rundir,lib.id,rundir,PREFIX, lib.id,rundir,PREFIX),"Scaffold")

           run_process("%s/toAmos_new -c %s/Assemble/out/%s.asm.tigr -b %s/Scaffold/in/%s.bnk "%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")
       elif asm == "metaidba":
          for lib in readlibs:
              run_process("%s/toAmos_new -s %s/Preprocess/out/lib%d.seq -m %s/Assemble/out/%s.lib%d.mappedmates -b %s/Scaffold/in/%s.bnk "%(AMOS,rundir,lib.id,rundir, PREFIX,lib.id,rundir,PREFIX),"Scaffold")
          run_process("%s/toAmos_new -c %s/Assemble/out/%s.asm.tigr -b %s/Scaffold/in/%s.bnk "%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")
       elif asm == "newbler":
          run_process("rm -rf %s/Scaffold/in/%s.bnk"%(rundir, PREFIX),"Scaffold")
          # build the bank for amos
          run_process("%s/bank-transact -b %s/Scaffold/in/%s.bnk -c -m %s/Assemble/out/%s.afg"%(AMOS,rundir, PREFIX, rundir, PREFIX),"Scaffold")
       elif asm == "velvet" or asm == "velvet-sc":
          run_process("rm -rf %s/Scaffold/in/%s.bnk"%(rundir, PREFIX), "Scaffold")
          run_process("%s/bank-transact -b %s/Scaffold/in/%s.bnk -c -m %s/Assemble/out/%s.afg"%(AMOS, rundir, PREFIX, rundir, PREFIX), "Scaffold")
       elif asm == "ca" or asm == "CA":
          run_process("%s/toAmos_new -a %s/Assemble/out/%s.asm -f %s/Assemble/out/%s.frg -b %s/Scaffold/in/%s.bnk -U "%(AMOS, rundir, PREFIX, rundir, PREFIX, rundir, PREFIX),"Scaffold")


   else:
       run_process("%s/bank-unlock %s/Scaffold/in/%s.bnk"%(AMOS,rundir,PREFIX))
       run_process("rm %s/Scaffold/in/%s.bnk/CTE.*"%(rundir,PREFIX),"SCAFFOLD")
       run_process("rm %s/Scaffold/in/%s.bnk/CTL.*"%(rundir,PREFIX),"SCAFFOLD")
       run_process("rm %s/Scaffold/in/%s.bnk/MTF.*"%(rundir,PREFIX),"SCAFFOLD")
       run_process("rm %s/Scaffold/in/%s.bnk/SCF.*"%(rundir,PREFIX),"SCAFFOLD")

   #calls to Bambus2, goBambus2 script
   # first, parse the parameters
   markRepeatParams = getProgramParams("bambus.spec", "MarkRepeats", "-")
   orientContigParams = getProgramParams("bambus.spec", "OrientContigs", "-")

   run_process("%s/clk -b %s/Scaffold/in/%s.bnk"%(AMOS,rundir,PREFIX),"Scaffold")
   run_process("%s/Bundler -b %s/Scaffold/in/%s.bnk"%(AMOS,rundir,PREFIX),"Scaffold")
   run_process("%s/MarkRepeats %s -b %s/Scaffold/in/%s.bnk > %s/Scaffold/in/%s.reps"%(AMOS,markRepeatParams,rundir,PREFIX,rundir,PREFIX),"Scaffold")
   run_process("%s/OrientContigs %s -b %s/Scaffold/in/%s.bnk -repeats %s/Scaffold/in/%s.reps "%(AMOS,orientContigParams,rundir,PREFIX, rundir, PREFIX),"Scaffold")

   # output results
   run_process("%s/bank2fasta  -b %s/Scaffold/in/%s.bnk > %s/Scaffold/out/%s.contigs"%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")
   run_process("%s/OutputMotifs -b %s/Scaffold/in/%s.bnk > %s/Scaffold/out/%s.motifs"%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")
   run_process("%s/OutputResults -b %s/Scaffold/in/%s.bnk -p %s/Scaffold/out/%s "%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")
   run_process("%s/OutputScaffolds -b %s/Scaffold/in/%s.bnk > %s/Scaffold/out/%s.scaffolds.final"%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")

   # generate linearize results
   run_process("%s/Linearize -b %s/Scaffold/in/%s.bnk"%(AMOS,rundir,PREFIX),"Scaffold")
   run_process("%s/OutputResults -b %s/Scaffold/in/%s.bnk -p %s/Scaffold/out/%s.linearize "%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")
   run_process("%s/OutputScaffolds -b %s/Scaffold/in/%s.bnk > %s/Scaffold/out/%s.linearize.scaffolds.final"%(AMOS,rundir,PREFIX,rundir,PREFIX),"Scaffold")


if "FindScaffoldORFS" in forcesteps:
    run_process("touch %s/Scaffold/out/%s.linearize.scaffolds.final"%(rundir,PREFIX))
@follows(Scaffold)
@files("%s/Scaffold/out/%s.linearize.scaffolds.final"%(rundir,PREFIX),"%s/FindScaffoldORFS/out/%s.scaffolds.orfs"%(rundir,PREFIX))
def FindScaffoldORFS(input,output):
   if "FindScaffoldORFS" in skipsteps:
      run_process("touch %s/FindScaffoldORFS/out/%s.scaffolds.faa"%(rundir, PREFIX))
      return 0

   run_process("%s/gmhmmp -o %s/FindScaffoldORFS/out/%s.scaffolds.orfs -m %s/config/MetaGeneMark_v1.mod -d -a %s/Scaffold/out/%s.linearize.scaffolds.final"%(GMHMMP,rundir,PREFIX,METAMOS_UTILS,rundir,PREFIX),"FindScaffoldORFS")
   parse_genemarkout("%s/FindScaffoldORFS/out/%s.scaffolds.orfs"%(rundir,PREFIX),1, "FindScaffoldORFS")
   #run_process("unlink %s/FindORFS/in/%s.scaffolds.faa"%(rundir,PREFIX))
   #run_process("ln -t %s/Annotate/in/ -s %s/FindORFS/out/%s.scaffolds.faa"%(rundir,rundir,PREFIX))

if "Propagate" in forcesteps:
    run_process("touch %s/DB/class_key.tab"%(rundir))
@follows(FindScaffoldORFS, Annotate)
@files("%s/DB/class_key.tab"%(rundir),"%s/Propagate/out/%s.clusters"%(rundir,PREFIX))
def Propagate(input,output):
   #run propogate java script
   # create s12.annots from Metaphyler output
   if cls == "metaphyler":
       run_process("python %s/python/create_mapping.py %s/DB/class_key.tab %s/Abundance/out/%s.classify.txt %s/Propagate/in/%s.annots"%(METAMOS_UTILS,METAMOS_UTILS,rundir,PREFIX,rundir,PREFIX),"Propagate")
   # strip headers from file and contig name prefix

   run_process("cat %s/Propagate/in/%s.annots |sed s/contig_//g |grep -v contigID > %s/Propagate/in/%s.clusters"%(rundir,PREFIX,rundir,PREFIX),"Propagate")
   run_process("%s/FilterEdgesByCluster -b %s/Scaffold/in/%s.bnk -clusters %s/Propagate/in/%s.clusters -noRemoveEdges > %s/Propagate/out/%s.clusters"%(AMOS,rundir,PREFIX,rundir,PREFIX,rundir,PREFIX),"Propagate")

@follows(Propagate)
@files("%s/Propagate/out/%s.clusters"%(rundir,PREFIX),"%s/Classify/out/sorted.txt"%(rundir))
def Classify(input,output):
   run_process("python %s/python/sort_contigs.py %s/Propagate/out/%s.clusters %s/DB/class_key.tab %s/Classify/out %s/Scaffold/in/%s.bnk"%(METAMOS_UTILS, rundir, PREFIX, METAMOS_UTILS,rundir, rundir, PREFIX),"Classify")

@follows(Classify)
@files("%s/Assemble/out/%s.asm.contig"%(rundir,PREFIX),"%s/Postprocess/%s.scf.fa"%(rundir,PREFIX))
def Postprocess(input,output):
#create_report.py <metaphyler tab file> <AMOS bnk> <output prefix> <ref_asm>
   #copy files into output for createReport   
   #generate reports
   #linearize
   #call KronaReports
   if cls == 'phmmer':
       if not os.path.exists(KRONA + os.sep + "ImportPHMMER.pl"):
          print "Error: Krona importer for PHMMER not found in %s. Please check your path and try again.\n"%(KRONA)
          raise(JobSignalledBreak)
       run_process("perl %s/ImportPHMMER.pl -c -v -i %s/Postprocess/in/%s.hits"%(KRONA,rundir,PREFIX),"Postprocess")
   elif cls == 'blast' or cls == 'metaphyler' or cls == None:
       if not os.path.exists(KRONA + os.sep + "ImportBLAST.pl"):
          print "Error: Krona importer for BLAST not found in %s. Please check your path and try again.\n"%(KRONA)
          raise(JobSignalledBreak)
       run_process("perl %s/ImportBLAST.pl -c -v -i %s/Postprocess/in/%s.hits"%(KRONA,rundir,PREFIX),"Postprocess")
   elif cls == 'fcp':
       print "FCP not supported yet ... stay tuned\n"
       #if not os.path.exists(KRONA + os.sep + "ImportFCP.pl"):
       #   print "Error: Krona importer for FCP not found in %s. Please check your path and try again.\n"%(KRONA)
       #   raise(JobSignalledBreak)
       #run_process("perl %s/ImportFCP.pl -c -v -i %s/Postprocess/in/%s.hits"%(KRONA,rundir,PREFIX),"Postprocess")
   elif cls == 'phymm':
       if not os.path.exists(KRONA + os.sep + "ImportPHYMM.pl"):
          print "Error: Krona importer for PHYMM not found in %s. Please check your path and try again.\n"%(KRONA)
          raise(JobSignalledBreak)
       run_process("perl %s/ImportPhymmBL.pl -c -v -i %s/Postprocess/in/%s.hits"%(KRONA,rundir,PREFIX),"Postprocess")
   elif cls == 'amphora':
       #now ran in Annotate step to generate file for Propogate/Classsify
       pass
       #if not os.path.exists(KRONA + os.sep + "ImportAmphora.pl"):
       #    print "Error: Krona importer for Amphora 2 not found in %s. Please check your path and try again.\n"%(KRONA)
       #    raise(JobSignalledBreak)
       #run_process("perl %s/ImportAmphora.pl -c -v -i %s/Postprocess/in/%s.hits:%s/Assemble/out/%s.contig.cvg"%(KRONA,rundir,PREFIX,rundir,PREFIX), "Postprocess") 

   #command to open webbrowser?
   #try to open Krona output
   if openbrowser:
       if os.path.exists(rundir + os.sep + "Postprocess" + os.sep + "out" + os.sep + "report.krona.html"):
           webbrowser.open_new("%s%sPostprocess%sout%sreport.krona.html"%(rundir, os.sep, os.sep, os.sep))
       else:
           print "ERROR: No Krona html file available! skipping"
   #webbrowser.open_new(output.html)
   #webbrowser.open_new_tab(output.html)
   run_process("cp %s/Abundance/out/%s.classify.txt %s/Postprocess/out/. "%(rundir,PREFIX,rundir),"Postprocess")
   run_process("cp %s/Scaffold/out/%s.linearize.scaffolds.final %s/Postprocess/out/%s.scf.fa"%(rundir,PREFIX,rundir,PREFIX),"Postprocess")
   run_process("ln -t %s/Postprocess/out/ -s %s/Scaffold/in/%s.bnk "%(rundir,rundir,PREFIX),"Postprocess")
   run_process("python %s/python/create_report.py %s/Abundance/out/%s.taxprof.pct.txt  %s/Postprocess/out/%s.bnk %s/Postprocess/out/ %s/Postprocess/out/%s.scf.fa %s %s"%(METAMOS_UTILS,rundir,PREFIX,rundir,PREFIX,rundir,rundir,PREFIX,METAMOS_UTILS,rundir),"Postprocess")   
   #webbrowser.open_new_tab(createreport.html)
   if openbrowser:
       if os.path.exists("%s/Postprocess/out/summary.html"%(rundir)):
           webbrowser.open_new_tab("%s/Postprocess/out/summary.html"%(rundir))
       else:
           print "ERROR: No Summary html file available! skipping"

def parse_metaphyler(giMapping, toTranslate, output):
   giDictionary = {};
   try:
      GIs = open(giMapping, 'r')
   except IOError as e:
      return
   for line in GIs:
      line = line.replace("\n","")
      splitLine = line.split("\t")
      giDictionary[splitLine[0]] = splitLine[1]
   GIs.close();
   try:
      GIs = open(toTranslate, 'r')
   except IOError as e:
      print "Exception opening file %s"%(e)
      return
   outf = open(output, 'w')
   for line in GIs:
      line = line.replace("\n","")
      splitLine = line.split("\t")
      if splitLine[1] in giDictionary:
         outf.write(line.replace(splitLine[1], giDictionary[splitLine[1]]) + "\n")
   GIs.close()
   outf.close()

def parse_genemarkout(orf_file,is_scaff=False, error_stream="FindORFS"):
    coverageFile = open("%s/Assemble/out/%s.contig.cvg"%(rundir, PREFIX), 'r')
    cvg_dict = {} 
    for line in coverageFile:
        data = line.split()
        cvg_dict[data[0]] = float(data[1])
    coverageFile.close()

    coords = open(orf_file,'r')
    coords.readline()
#    outf = open("proba.orfs",'w')
    prevhdr = 0
    prevhdraa = 0
    prevhdrnt = 0

    curcontig = ""
    curseqaa = ""
    curseqnt = ""
    reads = {}
    gene_dict = {}
    fna_dict = {}
    for line in coords:
        if ">gene" in line[0:10]:
            if "_nt|" in line:
                #print prevhdraa, prevhdrnt#, curseqaa, curseqnt
                if prevhdraa and curseqaa != "":
                    try:
                        gene_dict[curcontig].append(curseqaa)
                    except KeyError:
                        gene_dict[curcontig] = []
                        gene_dict[curcontig].append(curseqaa)
                    curseqaa = ""

                elif prevhdrnt and curseqnt != "":
                    try:
                        fna_dict[curcontig].append(curseqnt)
                    except KeyError:
                        fna_dict[curcontig] = []
                        fna_dict[curcontig].append(curseqnt)
                    curseqnt = ""

                prevhdrnt = 1
                prevhdraa = 0

            elif "_aa|" in line:

                if prevhdrnt and curseqnt != "":
                    try:
                        fna_dict[curcontig].append(curseqnt)
                    except KeyError:
                        fna_dict[curcontig] = []
                        fna_dict[curcontig].append(curseqnt)
                    curseqnt = ""
                elif prevhdraa and curseqaa != "":
                    try:
                        gene_dict[curcontig].append(curseqaa)
                    except KeyError:
                        gene_dict[curcontig] = []
                        gene_dict[curcontig].append(curseqaa)
                    curseqaa = ""
                prevhdraa = 1
                prevhdrnt = 0

            prevhdr = 1
            lined = line.replace("\n","")
            data = line[1:].split(">",1)[1]
            
            curcontig = data.split(" ")[0]
            if len(data.split(" ")) == 1:
                curcontig = data.split("\t")[0]
            curcontig = curcontig.strip()
            #print curcontig, len(curcontig)
            prevhdr = 1

        elif len(line) > 2 and prevhdraa == 1 and prevhdr:
            curseqaa += line
        elif len(line) > 2 and prevhdrnt == 1 and prevhdr:
            curseqnt += line
        elif len(line) <= 2 or "Nucleotide" in line: #and prevhdr == 1:
            prevhdr = 0
            #prevhdraa = 0
            #prevhdrnt = 0

        else:
            continue
    if prevhdraa and curseqaa != "":
        try:
          gene_dict[curcontig].append(curseqaa)
        except KeyError:
          gene_dict[curcontig] = []
          gene_dict[curcontig].append(curseqaa)
          curseqaa = ""

    elif prevhdrnt and curseqnt != "":
        try:
          fna_dict[curcontig].append(curseqnt)
        except KeyError:
          fna_dict[curcontig] = []
          fna_dict[curcontig].append(curseqnt)
    if is_scaff:
        outf = open("%s/FindScaffoldORFS/out/%s.faa"%(rundir,PREFIX),'w')
        outf2 = open("%s/FindScaffoldORFS/out/%s.fna"%(rundir,PREFIX),'w')
        #cvgf = open("%s/FindScaffoldORFS/out/%s.contig.cvg"%(rundir,PREFIX),'w')
        cvgg = open("%s/FindScaffoldORFS/out/%s.gene.cvg"%(rundir,PREFIX),'w')
    else:
        outf = open("%s/FindORFS/out/%s.faa"%(rundir,PREFIX),'w')
        outf2 = open("%s/FindORFS/out/%s.fna"%(rundir,PREFIX),'w')
        #cvgf = open("%s/FindORFS/out/%s.contig.cvg"%(rundir,PREFIX),'w')
        cvgg = open("%s/FindORFS/out/%s.gene.cvg"%(rundir,PREFIX),'w')
    #print len(gene_dict.keys())
    orfs = {}

    for key in gene_dict.keys():
        genecnt = 1

        if not is_scaff:
            if key in cvg_dict:
                cvgg.write("%s_gene%d\t%s\n"%(key,genecnt,cvg_dict[key])) 
            else:
                cvgg.write("%s_gene%d\t%s\n"%(key,genecnt, 1.0))
        for gene in gene_dict[key]:
            #min aa length, read depth
            if len(gene) < 100:# or cvg_dict[key] < 5:
                continue
            try:
                #print "contig"+key
                orfs["%s"%(key)] +=1
            except KeyError:
                orfs["%s"%(key)] =1
            outf.write(">%s_gene%d\n%s"%(key,genecnt,gene))

            genecnt +=1
    for key in fna_dict.keys():
        for gene in fna_dict[key]:
            if len(gene) < 300:# or cvg_dict[key] < 5:
                continue
            outf2.write(">%s_gene%d\n%s"%(key,genecnt,gene))
#        print gene_dict[key][0]
    outf.close()
    cvgg.close()
def parse_phmmerout(phmmerout):

    hit_dict = {}
    #phmout = open("%s.phm.tbl"%(prefix),'r')
    phmout = open(phmmerout,'r')
    phmmer_hits = {}
    ctghits = {}
    annot = {}
    for line in phmout:
        line = line.replace("\n","")

        if "gene" in line:
            tts = line.split("[",1)
            if len(tts) < 2:
                 phage_annot = "NA"
            else:
                 line,phage_annot = line.split("[",1)
            phage_annot = phage_annot.replace("]","")
            data = line.split(" ")
            data2 = []
            for item in data:
                if item == "" or item == "-" or item == "\n":
                    continue
                else:
                    data2.append(item)
            try:
                data2[16]
                for git in data2[16:]:
                    phage_annot += " "+git + " "

            except IndexError:
                pass

            data2 = data2[:15]
            #print phage_annot
            #print data2
            #print data2[1].split("_",1)[0]
            try:
                ctghits[data2[1]]
                continue
            except KeyError:
                ctghits[data2[1]] = 1
                pass
            phage_annot = phage_annot.replace(",","")
            try:
                annot[data2[1].split("_",1)[0]] += phage_annot
            except KeyError:
                annot[data2[1].split("_",1)[0]] = phage_annot
            try:
                phmmer_hits[data2[1].split("_",1)[0]] +=1
            except KeyError:
                phmmer_hits[data2[1].split("_",1)[0]] = 1
            try:
                hit_dict[data2[1]]
            except KeyError:
                hit_dict[data2[1]] = [float(data2[2]),int(float(data2[3])),phage_annot]
    #print len(hit_dict.keys())
    #for key in hit_dict.keys():
    #    print hit_dict[key]

if __name__ == "__main__":
    #pid = start_http()
    print "Starting metAMOS pipeline"
    guessPaths()

    try:
       #files = os.listdir(".")
       dlist = []
       pipeline_printout(sys.stdout,[Preprocess,Assemble, FindORFS, FindRepeats, Annotate, Abundance, Scaffold, FindScaffoldORFS, Propagate, Classify, Postprocess], verbose=1)
       pipeline_printout_graph (   'flowchart.svg',
                            'svg',
                            [Postprocess],
                            no_key_legend = True)
       pipeline_run([Preprocess,Assemble, FindORFS, FindRepeats, Annotate, Abundance, Scaffold, FindScaffoldORFS, Propagate, Classify, Postprocess], verbose = 1) 
       #multiprocess threads
       t2 = time.time()#clock()
       elapsed = float(t2)-float(t1)
       #print elapsed
       print "done! pipeline took %.2f minutes"%(float(elapsed)/float(60.0))
    except JobSignalledBreak:
       print "Done with errors\n"
