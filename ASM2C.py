import json
import instructionset

instructiondata={
	"adc": instructionset.adc,
	"and": instructionset.and1,
	"asl": instructionset.asl,
	"bcc": instructionset.bcc,
	"bcs": instructionset.bcs,
	"beq": instructionset.beq,
	"bit": instructionset.bit,
	"bmi": instructionset.bmi,
	"bne": instructionset.bne,
	"bpl": instructionset.bpl,
	"clc": instructionset.clc,
	"cld": instructionset.cld,
	"cmp": instructionset.cmp,
	"cpx": instructionset.cpx,
	"cpy": instructionset.cpy,
	"dec": instructionset.dec,
	"dex": instructionset.dex,
	"dey": instructionset.dey,
	".dw": instructionset.dw1,
	"eor": instructionset.eor,
	"inc": instructionset.inc,
	"index": instructionset.index,
	"inx": instructionset.inx,
	"iny": instructionset.iny,
	"jmp": instructionset.jmp,
	"jsr": instructionset.jsr,
	"lda": instructionset.lda,
	"ldx": instructionset.ldx,
	"ldy": instructionset.ldy,
	"lsr": instructionset.lsr,
	"mem": instructionset.mem,
	"ora": instructionset.ora,
	"org": instructionset.org,
	"pha": instructionset.pha,
	"pla": instructionset.pla,
	"rol": instructionset.rol,
	"ror": instructionset.ror,
	"rti": instructionset.rti,
	"rts": instructionset.rts,
	"sbc": instructionset.sbc,
	"sec": instructionset.sec,
	"sei": instructionset.sei,
	"sta": instructionset.sta,
	"stx": instructionset.stx,
	"sty": instructionset.sty,
	"tax": instructionset.tax,
	"tay": instructionset.tay,
	"txa": instructionset.txa,
	"txs": instructionset.txs,
	"tya": instructionset.tya
}


def main():
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
							if not instructions.get(counter).get("jumplocation")==None:
								instructions[counter]["dbloc"]=instructions[counter]["jumplocation"]
								del instructions[counter]["jumplocation"]
							instructions[counter][".db"].append(temp[x].strip(","))
							
						else:
							instructions[counter][".db"].append(temp[x].strip(","))
							skipcounter=True
				else:
					if temp[0].strip()==".index":
						temp[0]="index"
					elif temp[0].strip()==".mem":
						temp[0]="mem"
					elif temp[0].strip()==".org":
						temp[0]="org"
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

		char memory[8192];
		int x=0;
		int y=0;
	"""

		

	for instruction in instructions:
		temp=instructions.get(instruction)
		if not temp.get("comment")==None:
			buffer=buffer + "\t// " + temp.get("comment") + "\n"
		if not temp.get("jumplocation")==None:
			buffer=buffer + "\t" + temp.get("jumplocation") + ":" + "\n"
		if not temp.get("instruction")==None:
			if not temp.get("instructionvalue")==None:
				#print(temp.get("instruction"))
				buffer=instructiondata.get(temp.get("instruction"))(buffer, temp.get("instructionvalue"))
			else:
				#print(temp.get("instruction"))
				buffer=instructiondata.get(temp.get("instruction"))(buffer)
	
	buffer=buffer + "\n\treturn 0;\n}"
	print(buffer)
	
if __name__ == "__main__":
	main()
