import socket
import struct
import textwrap

TAB1 = '\t - '
TAB2 = '\t\t - '
TAB3 = '\t\t\t - '
TAB4 = '\t\t\t\t - '

DATA_TAB1 = '\t '
DATA_TAB2 = '\t\t '
DATA_TAB3 = '\t\t\t '
DATA_TAB4 = '\t\t\t\t '


def main():
	conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
	while True:
		raw_data, addr = conn.recvfrom(65536)
		dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
		print('\nEthernet Frame:')
		print(TAB1 + 'Destination: {}, Source {}, Protocol {}'.format(dest_mac, src_mac, eth_proto))

		if eth_proto == 8:
			pass



# Unpack ethernet frame 
def ethernet_frame(data):
	dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
	return getMacAddr(dest_mac), getMacAddr(src_mac), socket.htons(proto), data[14:]

# Returns properly formatted MAC Address (AA:BB:CC:DD:EE:FF)
def getMacAddr(bytesAddr):
	bytesStr = map('{:02x}'.format, bytesAddr)
	return ':'.join(bytesStr).upper()


# Unpack TCP segment
def tcp_segment(data):
	(src_port,dest_port, sequence, ackgmnt, flags) = struct.unpack('! H H L L H', )
	offset = (flags >> 12) * 4
	flag_urg = (flags & 32) >> 5
	flag_ack = (flags & 16) >> 4
	flag_psh = (flags & 8) >> 3
	flag_rst = (flags & 4) >> 2
	flag_syn = (flags & 2) >> 1
	flag_fin = (flags & 1)
	return src_port, dest_port, sequence, ackgmnt, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, 

# Unpack UDP segment
def udp_segment(data):
	src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
	return src_port, dest_port, size, data[8:]

def format_multi_line(prefix, string, size=80):
	size = len(prefix)
	if isinstance(string, bytes):
		string = ''.join(r'\x{:02x}'.format(bytes) for byte in bytes)
		if size % 2:
			size -= 1
	return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

main()