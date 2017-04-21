
#
# This Python program prepares parent folder fullpaths for the objects.
# This can be useful when parent paths have to be recreated because VerifyObjectTask cannot handle it e.g version 3.1.130
# Program needs 2 input files
# - bucketsInFile: file with full paths of required buckets. This will be needed to rebuild fullpath for the object
# - objectsInFile: file with object IDs (one object ID per line)
#
# Additional parameter is a path prefix that needs to be added to rebuilt path
#
# Sample input (bucketsInFile):
# 	/opt/matrixstore/root/blobs1/38297147-5994-11e5-abaf-e922c70c4afe/1a203c94-86ed-11e6-af2a-afe9c1d2f8b2
# 	/opt/matrixstore/root/blobs1/e26268ca-9150-11e6-84ed-aa77adbc5732/1ac8a01c-0fc1-11e7-a023-a207bb9da2ac
# From bucketsInFile file vaultId and bucket ID are extracted (last 2 elements), so at least those should be in there.
#
# Sample input (objectsInFile):
#	ddc2ee0f-0fbb-11e7-9d7a-979b6f5f6e76-8184
#	ddc2ee0f-0fbb-11e7-9d7a-979b6f5f6e76-8192
#	df845bc7-0a34-11e7-a023-a207bb9da2ac-24
#	df845bc7-0a34-11e7-a023-a207bb9da2ac-25
# From objectsInFile full object ID is used. Object Id should not be prefixed/ suffixed with any string
#
# Program outputs all rebuilt paths to a standard output, to be redirected to a file > myfile.txt and used for further processing eg. with
#	while read l; do sudo mkdir -p $l; done < myfile.txt
#
# Sample output:
#
# /solidstate/media/ARRAY1/blobs1/e26268ca-9150-11e6-84ed-aa77adbc5732/ddc2ee0f-0fbb-11e7-9d7a-979b6f5f6e76/3/9/8
# /solidstate/media/ARRAY1/blobs1/e26268ca-9150-11e6-84ed-aa77adbc5732/ddc2ee0f-0fbb-11e7-9d7a-979b6f5f6e76/3/9/B
# /solidstate/media/ARRAY1/blobs1/e26268ca-9150-11e6-84ed-aa77adbc5732/ddc2ee0f-0fbb-11e7-9d7a-979b6f5f6e76/3/A/0
#
# Changelog:
# 2017-03-28	1.1
#	- changed input file name to objects.txt
# 2017-03-28	1.0
#	- initial version
#

bucketsInFile="buckets.txt"
objectsInFile="objects.txt"
pathPrefix="/solidstate/media/ARRAY1/blobs1/"

def bucketmap(filepath):
	bid2path = {}
	file = open(filepath, "r")
	for line in file:
		line=line.strip()
		if len(line) > 0:
			# print line
			a=line.split('/')
			# print "buck ",a[-1]," path: ",line
			sub=a[-2]+"/"+a[-1]
			# print "sub: ",sub
			bid2path[a[6]]=sub
	file.close()
	return bid2path

def convert_to_base12(num):
    num = int(num)
    sbl = '0123456789AB'
    base = 12

    neg = False
    if num < 0:
        neg = True
        num = -num

    num, rem = divmod(num, base)
    ret = ''
    while num:
        ret = '/' + sbl[rem] + ret
        num, rem = divmod(num, base)
    ret = ('-' if neg else '') + sbl[rem] + ret
    if len(ret) == 1:
    	ret = "0/0/0/"+ret
    elif len(ret) == 3:
    	ret = "0/0/"+ret
    elif len(ret) == 5:
    	ret = "0/"+ret
    return ret

def base12_to_decimal(num):
  return int(num, 12)

def oidpath(filepath):
	oids=[]
	file = open(filepath, "r")
	for line in file:
		line=line.strip()
		if len(line) > 0:
			# print line
			bucket=line[0:36]
			serial=line[37:]
			b12 = convert_to_base12(serial)
			# print "bucket: ",bucket,"serial: ",serial,"base12:",b12
			oids.append((bucket,b12))
	file.close()
	return oids


def process():
	paths=[]
	for o in oids:
		bucket=o[0]
		bpath=bid2path[bucket]
		spath=o[1]
		spath=spath[0:5]
		# print "Process",o,"fullpath /solidstate/media/ARRAY1/"+bpath+"/"+spath
		fpath=pathPrefix+bpath+"/"+spath
		paths.append(fpath)

	pathsSet=set(paths)
	sortedPaths=sorted(pathsSet)

	for p in sortedPaths:
		print p

bid2path = bucketmap(bucketsInFile);
oids = oidpath(objectsInFile)

process()




