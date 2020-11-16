import csv
import os
import sys
import platform


print platform.node()

spectrometers = {'DM-CHEM-200': 'B4',
                 'ERIC-PC': 'B4',
                 'clevinger': 'B4',
                 'mudd': 'N4',
                 'mcwatt': 'A4'}

solvents = {'N4': {'chloroform' : 'CDCl3',
                   'DMSO' : 'DMSO',
                   'D2O' : 'D2O',
                   'Acetic Acid': 'Acetic',
                   'acetone': 'acetone',
                   'benzene': 'C6D6',
                   'dichloromethane': 'CD2Cl2',
                   'acetonitrile': 'CD3CN',
                   'DMF': 'DMF',
                   'dioxane': 'Dioxane',
                   'ethanol': 'EtOD',
                   'H2O+D2O': 'H2O+D2O',
                   'HDMSO': 'HDMSO',
                   'methanol': 'MeOD',
                   'no solvent': 'None'},

          'A4': {'chloroform' : 'CDCl3',
                 'DMSO' : 'DMSO',
                 'D2O' : 'D2O',
                   'Acetic Acid': 'Acetic',
                   'acetone': 'Acetone',
                   'benzene': 'C6D6',
                   'dichloromethane': 'CD2Cl2',
                   'acetonitrile': 'CD3CN',
                   'DMF': 'DMF',
                   'dioxane': 'Dioxane',
                   'ethanol': 'EtOD',
                   'H2O+D2O': 'H2O+D2O',
                   'HDMSO': 'HDMSO',
                   'methanol': 'MeOD',
                   'no solvent': 'None'},

          'B4': {'chloroform' : 'CDCl3',
                 'DMSO' : 'DMSO',
                 'D2O' : 'D2O',
                 'Acetic Acid': 'Acetic',
                 'acetone': 'Acetone',
                 'benzene': 'C6D6',
                 'dichloromethane': 'CD2Cl2',
                 'acetonitrile': 'CD3CN',
                 'DMF': 'DMF',
                 'dioxane': 'Dioxane',
                 'ethanol': 'EtOD',
                 'H2O+D2O': 'H2O+D2O',
                 'HDMSO': 'HDMSO',
                 'methanol': 'MeOD',
                 'no solvent': 'None'}}

experiments = {'N4': {'proton': 'N Proton1.icon',
                      'carbon': 'N Carbon.dur',
                      'dept': 'N DEPT135.dur',
                      '31P': 'N P31.d',
                      '31P  Decouple': 'N P31CPD.d',
                      '31P wide': 'N P31.d_wide',
                      '31P wide Decouple': 'N P31CPD.d_wide',
                      'cosy': "C COSY1.icon"},

               'A4': {'proton': 'N Proton.dur',
                      'carbon': 'n Carbon.dur',
                      'dept': 'N Dept135.dur',
                      '31P': 'N P31.d',
                      '31P  Decouple': 'N P31CPD.d',
                      '31P wide': 'N P31.d_wide',
                      '31P wide Decouple': 'N P31CPD.d_wide',
                      'cosy': 'C COSY',
                      '19F sweep': 'C 19F_Sweep_Width',
                      '11B': 'N B11.dur',
                      '11B Decouple': 'N B11_PRODEC.dur',
                      '11B Unlocked': 'N B11_unlocked.dur',
                      '11B Unlocked Decouple': 'N B11_PRODEC_unlocked.dur'},

               'B4': {'proton': 'N Proton.dur',
                      'carbon': 'n Carbon.dur',
                      'dept': 'n DEPT135.dur',
                      '31P': 'N P31.d',
                      '31P  Decouple': 'N P31CPD.d',
                      '31P wide': 'N P31 wide.d',
                      '31P wide Decouple': 'N P31CPD wide.d',
                      'cosy': 'C COSY',
                      '19F sweep': 'C 19F_Sweep_Width',
                      '11B': 'N B11.dur',
                      '11B Decouple': 'N B11_PRODEC.dur',
                      '11B Unlocked': 'N B11_unlocked.dur',
                      '11B Unlocked Decouple': 'N B11_PRODEC_unlocked.dur',
                      '11B COSY': 'C 11B_COSY',
                      '11B HMQC': 'C 11B_HMQC',
                      '7Li Standard': 'Li7.dur'}}

# 'N4': "/data/downloads/Eric"
# 'B4': r"c:\Bruker\Topspin4.0.8\exp\stan\nmr\py\user"

if platform.node() == 'DM-CHEM-200':
    downloads_dir = {'B4': r"w:\downloads\Eric\jython",
                     'A4': "/data/downloads/Eric",
                     'N4': "/data/downloads/Eric"}

    auto_dir = {'N4': "/opt/topspin4.0.6/prog/tmp",
                'A4': "/opt/topspin3.2_pl3/prog/tmp",
                'B4':  r"w:\downloads\Eric\jython"}

elif platform.node() == 'ERIC-PC':
    downloads_dir = {'B4': r"C:\Users\ERIC\Dropbox\projects\programming\2020\python\autoNMRinput",
                     'A4': "/data/downloads/Eric",
                     'N4': "/data/downloads/Eric"}
                     
    auto_dir = {'N4': "/opt/topspin4.0.6/prog/tmp",
                'A4': "/opt/topspin3.2_pl3/prog/tmp",
                'B4':  r"C:\Users\ERIC\Dropbox\projects\programming\2020\python\autoNMRinput"}
else:
    downloads_dir = {'B4': "/data/downloads/Eric",
                     'A4': "/data/downloads/Eric",
                     'N4': "/data/downloads/Eric"}

    auto_dir = {'N4': "/opt/topspin4.0.6/prog/tmp",
                'A4': "/opt/topspin3.2_pl3/prog/tmp",
                'B4':  "/opt/topspin3.2_pl3/prog/tmp"}
                
                
computer_name = platform.node()
spec_name = spectrometers[computer_name]

def return_auto_fn( fn, directory ):

    path_nm, file_nm = os.path.split(fn)
    fn_main, fn_ext = os.path.splitext(file_nm)

    return os.path.join( directory, fn_main + ".txt" )

class CommandLineArgs:
    
    def __init__(self, argv):
        self.data = argv[0]
        self.fn = argv[1]
        self.holder_offset = int(argv[2])


def submitNMRexpts( argv ):
     
    try:
        print argv[-1]
        int(argv[-1])
    except:
        print "Last command line parameter should be an integer for the carousel position"
        return 1
        
    args = CommandLineArgs(argv)

    computer_name = platform.node()
    spec_name = spectrometers[computer_name]

    fn = os.path.join(  downloads_dir[spec_name], args.fn )
    auto_fn = return_auto_fn( fn, auto_dir[spec_name] )

    # read in csv file and store as a list of dictionaries
    # one dictionary for each line
    # expt_list = []
    # f = open(fn, 'r')
    # reader = csv.DictReader(f)
    # for row in reader:		
    #     expt_list.append(row)
    # f.close()
    
    # Check to see if all experiments can be run chosen spectrometers
    # if not, output an error message 
    # and do not start creating NMR automation file
    ok_to_run = True
    for expt in args.data:
        #
        # check to see if pulse sequence will run on current spectrometer
        # skip any high field cases
        if expt[3] == "High Field":
            continue
        if expt[3] not in experiments[spec_name].keys():
            ok_to_run = False
            errorNumber= 2
            error_message = 'Experiment \"' + expt[3] + '\" can not be run on spectrometer ' + spec_name
            print ""
            print "------------------------- Error ---- Error ------------------------------------"
            print ""
            print error_message
            print 'Choose a different spectrometer'
            print 'Program Quitting!!!'
            print ""
            print "-------------------------------------------------------------------------------"
            print ""
            return errorNumber

    # Check that holder offset is a positive integer greater than 0 and less than 61
    for expt in args.data:
        if (int(expt[1]) < 1) and (expt[3] != "High Field") or (int(expt[1]) > 60):
            # ok_to_run = False
            errorNumber = 3
            error_message = 'A Holder starting position is \"' + str(expt[1]) +  '\"  it should be between 1 and 60 inclusive'
            print ""
            print "------------------------- Error ---- Error ------------------------------------"
            print ""
            print error_message
            print 'Choose a different starting position in the carousel'
            print 'Program Quitting!!!'
            print ""
            print "-------------------------------------------------------------------------------"
            print ""
            return errorNumber

    # Check to see that carousel starting position is compatible with the number of samples to be run
    # ie holder_offset should be chosen so that last sample position is equal or less than 60   
    # last_sample_position = args.holder_offset - 1 + int(expt_list[-1]['sample #'])
    if int(args.data[-1][1]) > 60:
        ok_to_run = False
        errorNumber = 4
        error_message = 'Too many samples for carousel starting position, last sample position exceeds 60\n'
        # error_message = error_message + 'Number of samples equals ' + expt_list[-1]['sample #'] + '\n'
        error_message = error_message + 'Carousel starting position equals ' + str(args.data[-1][1])
        print ""
        print "-------------------------------- Error ---- Error ---------------------------------------"
        print ""
        print error_message
        print ""
        print 'Choose a different starting position in the carousel'
        print 'Program Quitting!!!'
        print ""
        print "-----------------------------------------------------------------------------------------"
        print ""		
        return errorNumber
        
    # create NMR automation txt file if all checks ok
    f = open(auto_fn, 'w')

    print "USER walkup"
    f.write( "USER walkup" +"\n" )
    
    holder_offset = args.holder_offset-1
    holder_old = 0

    for expt in args.data:
        #
        # if expt for high field skip it
        if expt[3] == "High Field":
            continue
        holder = expt[1]
        name = expt[2]
        solvent = expt[4]
        title = expt[5] + ':' + expt[6] + ':' + expt[7]
        experiment = expt[3]
        if holder_old != holder:
            print "#"
            print "HOLDER " + str(holder)
            print "NAME " + name
            print "EXPNO 10"
            print "SOLVENT " + solvents[spec_name][solvent]
            print "EXPERIMENT " +  experiments[spec_name][experiment] 
            print "TITLE " + title
            
            f.write("#" +"\n")
            f.write( "HOLDER " + str(holder) +"\n")
            f.write("NAME " + name +"\n")
            f.write("EXPNO 10" +"\n")
            f.write("SOLVENT " + solvents[spec_name][solvent] +"\n")
            f.write("EXPERIMENT " +  experiments[spec_name][experiment] +"\n")
            f.write("TITLE " + title +"\n")
            
            holder_old = holder
        else:
            print "EXPERIMENT " +  experiments[spec_name][experiment] 
            print "TITLE " + title
            
            f.write("EXPERIMENT " +  experiments[spec_name][experiment] +"\n") 
            f.write("TITLE " + title +"\n")
    print "#"
    print "END"
    
    f.write("#\n")
    f.write("END\n")
    f.close()

    # write out CSV file again but now with holder position column
    # and spectrometer used
        
    # for expt in expt_list:
    #     expt['Holder'] = int(expt['sample #']) + args.holder_offset - 1
    #     expt['Spectrometer'] = spec_name
        
    print "fn", fn
    s1, s2 = fn.rsplit('.', 1)
    fn2 = s1 + '_' + spec_name + '.' + s2
    print fn2


    csvfile = open(fn2, 'w')
    fieldnames = ['sample #',
                  'Holder',
                  'Name',
                  'Experiment',
                  'Solvent',
                  'Group',
                  'Member',
                  'Sample Name']
                  
    csvfile.write(','.join(fieldnames))
    csvfile.write('\n')
    
    for expt in args.data:
        csvfile.write(','.join([ str(v) for v in expt]))
        csvfile.write('\n')
        
    # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # for expt in expt_list:
    #     writer.writerow(expt)
        
    csvfile.close()
    
    return 0
        







