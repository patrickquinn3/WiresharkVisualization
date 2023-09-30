# The purpose of this program is to visualize wireshark pcap
# files to show the source and destination on a global map

# Libraries
import dpkt
import socket
import pygeoip

# variable with root to GeoLiteCity Database
gi = pygeoip.GeoIP(r'C:\x\GeoLiteCity.dat') # replace x with correct root

# Attach geo location to data then convert to kml format
def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('x.x.x.x') # Source IP, replace x's with personal IP
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''

# Loops over captured network data and extracts IP
def plotIPs(pcap):
        kmlPts = ''
        for(ts, buf) in pcap:
                try:
                        eth = dpkt.ethernet.Ethernet(buf)
                        ip = eth.data
                        src = socket.inet_ntoa(ip.src) # Source
                        dst = socket.inet_ntoa(ip.dst) # Destination
                        KML = retKML(dst, src)
                        kmlPts = kmlPts + KML
                except:
                    pass
        return kmlPts

# Opens captured data, creates kml header and footer
def main():
    # opens pcap file
    f = open(r'C:\x\example.pcap', 'rb') # replace x with correct root and example pcap with pcap filename
    pcap = dpkt.pcap.Reader(f)
    
    # kml used to style the map presented in Google MyMaps
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    print(kmldoc)

# Execute above code to print kml file in terminal
if __name__ == '__main__':
    main()