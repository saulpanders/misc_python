# @saulpanders
# nmap_parser.py
# 
# parses the output from an nmap scan into a .CSV file (Host, Up/down, port, service info, version #)
# code is pretty ugly ngl but wanted to try my hand at an nmap parser
# Using a dict to store info (uniquely) by host
# ref: https://nmap.org/book/man-output.html
# 
#	host_object = 
#	{
#		"ip": 192.168.1.1
#		"host": hostname
#		"status": up/down
#		"os: Win 7 etc
#		"ignored_stage": # ignored
#		"ports": [{
#			"port_num":
#			"state":
#			"protocool":
#			"owner":
#			"service":
#			"sunRPC":
#			"version":
#		}]
#	}
# hosts = 
#		{
#			"192.168.1.1" = host_obj
#			"192.168.1.2" = host_obj_2
#			etc			
#		}
#	
#	
#
import argparse




def file_in(infile):
	hosts = {}
	##parse input in to return as dictionary
	with open(infile) as f:
		for line in f:
			## definiting host obj variable
			host_obj = line.split()[1]
			try:
				if(hosts[host_obj]):
					pass
			except:
				hosts[host_obj] = {"ip": host_obj, "hostname": line.split()[2]}
				pass
			finally:
				line_arr = line.split()
				if ("Status" in line):
					hosts[host_obj]['status'] = line_arr[line_arr.index("Status:") + 1]
				
				#this is jank - added else clause to deal with blanks
				if ("Ignored State" in line):
					hosts[host_obj]['ignored_state'] = line_arr[line_arr.index("Ignored") + 3]
				else:
					hosts[host_obj]['ignored_state'] = "null"
				
				#OS parsing - ditto to above
				if ("OS:" in line):
					hosts[host_obj]['os'] = line_arr[line_arr.index("OS:") + 1]
				else:
					hosts[host_obj]['os'] = "null"
				
				#port parsing
				if ("Ports" in line):
					p_arr = []
					for p in [x for x in line_arr if "/" in x]:
						p_enum = p.split("/")
						if p_enum[0].isdigit():
							p_temp = { "port_num": p_enum[0], "state": p_enum[1], "protocol": p_enum[2], "owner": p_enum[3], "service": p_enum[4], "sunRPC": p_enum[5], "version": p_enum[6]}
							p_arr.append(p_temp)

					hosts[host_obj]['ports'] = p_arr
	return hosts


# Ton on on-the-fly string building... if I could start all over I probably would
def file_out(host_list, outfile_name, delimiter):

    with open(outfile_name, "w+") as f:
    	#define columns for CSV
        column_string = "IP" + delimiter + "Hostname" + delimiter + "Status" + delimiter +  "Ignored State" + delimiter + "OS" + delimiter + "Port" + delimiter +  "Port State" + delimiter + "Protocol" + delimiter + "Owner" + delimiter + "Service" + delimiter + "sunRPC" + delimiter + "Version" + ""
        f.write(column_string + "\n")

        #loop through host dicts in host_list
        for host_object in host_list:
        	host_string = ""
        	#loop through per-host portscan attributes
        	for attribute in host_list[host_object]:
        		#if this is the port summaries, handle separately
        		if isinstance(host_list[host_object][attribute], list):
        			port_string = ""
        			#loop through each portsum and parse out port info
        			for port_summary in host_list[host_object][attribute]:
        				port_string = "".join([port_summary[x] + delimiter for x in port_summary])
        				port_string = host_string + port_string
        				f.write(port_string + "\n")

        		else:
        			host_string = host_string + host_list[host_object][attribute] + delimiter
	

def main():
    parser = argparse.ArgumentParser(description='Nmap results parser')
    parser.add_argument('-i', '--input', type=str, help="Nmap results to parse (only takes .gnmap)")
    parser.add_argument('-o', '--output', type=str, help='Output file name', default="results.csv")
    parser.add_argument('-d', '--delimiter', type=str, help = "Field delimiter (default: ,)", default=",")
    args = parser.parse_args()
    
    #set delimiter if not set
    if not args.delimiter:
        args.delimiter = ','

    #parse infile
    hosts_summary = file_in(args.input)

    #get rid of first line "Nmap 7.80 etc"
    del hosts_summary['Nmap']

    #write to outfile
    file_out(hosts_summary, args.output, args.delimiter)





if __name__ == "__main__":
	main()