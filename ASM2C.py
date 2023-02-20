import json

debug=False

f=open("smb.asm", "r")
data=f.read().split("\n")

# The folloowing code converts the ASM to a Dictionary
instructions={}
counter=1
skipcounter=False
linenumber=0
for line in data:
	linenumber+=1
	temp=line.split(";", 1)
	if skipcounter==False:
		instructions[counter]={}	
	skipcounter=False
	if len(temp)>1:
		instructions[counter]["comment"]=temp[1].strip()
	newdata=temp[0]
	temp=newdata.split("=")
	if len(temp)>1:
		instructions[counter]["variable"]=temp[0].strip()
		instructions[counter]["variablevalue"]=temp[1].strip()
	else:
		newdata=temp[0]
		temp=newdata.split(":")
		if len(temp)>1:
			if len(temp)>1:
				instructions[counter]["jumplocation"]=temp[0].strip()
				newdata=temp[1].strip()
				skipcounter=True
			else:
				newdata=temp[0].strip()
		temp=newdata.strip().split(" ")

		if len(temp)>1:
			if temp[0]==".db":
				for x in range(1, len(temp)):
					if instructions.get(counter).get(".db")==None:
						instructions[counter][".db"]=[]
						instructions[counter][".db"].append(temp[x].strip(","))
						
					else:
						instructions[counter][".db"].append(temp[x].strip(","))
						skipcounter=True
			else:
				instructions[counter]["instruction"]=temp[0].strip()
				instructions[counter]["instructionvalue"]=temp[1].strip()
				skipcounter=False
		else:
			if not temp[0]=="":
				instructions[counter]["instruction"]=temp[0].strip()
				skipcounter=False
		#print(temp)
			
		
	if skipcounter==False:					
		counter=linenumber
			
if debug==True:
	print(json.dumps(instructions, indent=4))
	
	
buffer="""#include <stdio.h>
#include <stdlib.h>
int main(void) {
	"""

for instruction in instructions:
	temp=instructions.get(instruction)
	if not temp.get("comment")==None:
		buffer=buffer + "\t// " + temp.get("comment") + "\n"
	
buffer=buffer + "\n\treturn 0;\n}"

print(buffer)
