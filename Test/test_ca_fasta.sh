#bzip2 -d test4.sff.bz2
../initPipeline -l flx -f -m carsonella_pe_filt.fna -d test_ca_fasta -i 3000:4000 
../runPipeline -c fcp -a ca -p 4 -d test_ca_fasta -k 55 -f Preprocess