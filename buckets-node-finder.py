
# Script finds nodes by volumes
# It extracts information from 3 files
# 1) bucksinregenfile
#	Comma separated list of buckets
# 2) bucketinriakfile
#	Buckets information taken from riak-inspector
# 3) volumes
#	Ordered by node number list of volume IDs, one per line
#	Assumes one volume per node
#
# Changelog:
#
# 2017-04-21	v1.0
#		- initial version
#
bucksinregenfile="buckets-list.txt"
bucketinriakfile="Buckets"
volumesfile="volumes.txt"

def loadbucketsinregen(filepath):
	bids = set()
	file = open(filepath, "r")
	for line in file:
		bucks=line.split(',')
		for b in bucks:
			b=b.strip()
			bids.add(b)
	file.close()
	return bids

# parse riak-inspector output file
# BUCK_002433c4-5ec8-11e4-a782-cb5464dd4de7	{"_volumeIds":["69449394-3e25-11e2-832d-f372b7e1d740","ead7af92-3e22-11e2-9530-d16311448c03"],"_entity":"002433c4-5ec8-11e4-a782-cb5464dd4de7"}
def loadriakbuckets(filepath):
	b2locs = {}
	file = open(filepath, "r")

	for line in file:
		if line.startswith("BUCK_"):
			split=line.split('"')
			# print split
			bid=split[9]
			v1=split[3]
			v2=split[5]
			# print "bid="+bid
			# print "v1="+v1
			# print "v2="+v2
			b2locs[bid]=v1,v2
	file.close()
	return b2locs

def loadvolumes(filepath):
	vol2node={}
	file = open(filepath, "r")

	i=1
	for line in file:
		vol=line.strip()
		if len(vol) > 0:
			vol2node[vol]="node"+str(i)
			i+=1

	file.close()
	return vol2node

bids=loadbucketsinregen(bucksinregenfile)
b2locs=loadriakbuckets(bucketinriakfile)
vols=loadvolumes(volumesfile)

# find nodes for volumes
for bid in bids:
	volsof=b2locs[bid]
	# print "Bucket",bid,"has volumes:",volsof
	v1=volsof[0]
	v2=volsof[1]
	if v1 in vols:
		nA=vols[v1]
	else:
		nA="unk"
	if v2 in vols:
		nB=vols[v2]
	else:
		nB="unk"
	print "Bucket",bid,"has volumes:",volsof,"which are nodes:",nA,nB


