import argparse
import os
import re

pol = {
        'md' : 'MagDown',
        'mu' : 'MagUp'
        }

parser = argparse.ArgumentParser(description='Merger')

parser.add_argument('jobid',
                 help = 'job id with outputfile .root')


args = parser.parse_args()
id = args.jobid

#CHECKING ERRORS
checker = (jobs(id).name.split(':')[1][0] == '1') 
if checker ==False:
    print("ERROR: You took the wrong job id")
    exit()

checker2 = (jobs(id).status == 'completed')
if checker2 == False:
    print("ERROR: The job has not yet finished")
    exit()

#Taking wildcards
name = tasks(int(jobs(id).name[1:4])).name
pattern = [
           r"(Bs2JpsiPhi|Bs2JpsiPhi_dG0|Lb2JpsipK|Bd2JpsiKstar)",
           r"(2015|2016|2017|2018)",
           r"(_sim09b|_sim09c|_sim09g|_sim09k|_sim09h|_sim09i|_sim09b_dst|_sim09b_ldst)",
           r"(_md|_mu)"
               ]
# pattern = [
#            r"(Bs2JpsiPhi|Bs2JpsiPhi_dG0|Lb2JpsipK|Bd2JpsiKstar)",
#            r"(2015|2016|2017|2018)",
#            r"(_sim09b|_sim09c|_sim09g|_sim09k|_sim09h)",
#            r"(_md|_mu)"
#                ]

pattern = rf"\A{''.join(pattern)}\Z"
p = re.compile(pattern)
mode, year, stripping, polarity = p.search(name).groups()
stripping = stripping[1:]
polarity = polarity[1:]
print(mode, year, stripping, polarity)

#Recollecting subjobs
input = ' '.join([s.outputdir+'DVntuple.root' for s in jobs(id).subjobs])

#Writting command in a script
open(f"sh_folder/MC_{mode}_{year}_{stripping}_{pol[polarity]}.sh", 'w').write(f"""#!/bin/bash
hadd -fk output/{mode}/MC_{mode}_{year}_{stripping}_{pol[polarity]}.root {input}
""")

