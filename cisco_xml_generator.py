#!/usr/bin/python3

import xml.etree.ElementTree as ET
from pprint import pprint
from xml.dom import minidom
import yaml

def extension(ext):
    extension = ET.SubElement(begin, 'Extension_{}_'.format(ext), attrib={'group':'Phone/Line_Key_{}_'.format(ext)})
    extension.text = str(ext)
    ext_short_name = ET.SubElement(begin, 'Short_Name_{}_'.format(ext), attrib={'group':'Phone/Line_Key_{}_'.format(ext)})
    ext_short_name.text = "Line{}".format(ext)
    ext_display_name = ET.SubElement(begin, 'Display_Name_{}_'.format(ext), attrib={'group':'Ext_{}/Subscriber_Information'.format(ext)})
    user_id = ET.SubElement(begin, 'User_ID_{}_'.format(ext), attrib={'group':'Ext_{}/Subscriber_Information'.format(ext)})
    password = ET.SubElement(begin, 'Password_{}_'.format(ext), attrib={'group':'Ext_{}/Subscriber_Information'.format(ext)})
    dialplan = ET.SubElement(begin, 'Dial_Plan_{}_'.format(ext), attrib={'group':'Ext_{}/Dial_Plan'.format(ext)})
    dialplan.text = "( [268]xxxxxxxxx | x. | [*#x][*#x]. | *x. | **x. | x.* | x.** | xx*xxxxxxxxxx )"
    
def ext_common(ext_common):
    share_call_appearance = ET.SubElement(begin, 'Share_Call_Appearance_{}_'.format(ext_common), attrib={'group':'Phone/Line_Key_{}'.format(ext_common)})
    share_ext = ET.SubElement(begin, 'Share_Ext_{}_'.format(ext_common, attrib={'group':'Ext_{}_/Share_Line_Appearance'.format(ext_common)}))
    nat_mapping_enable = ET.SubElement(begin, 'NAT_Mapping_Enable_{}_'.format(ext_common), attrib={'group':'Ext_{}_/NAT_Settings'.format(ext_common)})
    nat_keep_alive_enable = ET.SubElement(begin, 'NAT_Keep_Alive_Enable_{}_'.format(ext_common), attrib={'group':'Ext_{}_/NAT_Settings'.format(ext_common)})
    sip_port = ET.SubElement(begin, 'SIP_Port_{}_'.format(ext_common), attrib={'group':'Ext_{}_/SIP_Settings'.format(ext_common)})
    proxy = ET.SubElement(begin, 'Proxy_{}_'.format(ext_common), attrib={'group':'Ext_{}_/Proxy_and_Registration'.format(ext_common)})
    register = ET.SubElement(begin, 'Register_{}_'.format(ext_common), attrib={'group':'Ext_{}_/Proxy_and_Registration'.format(ext_common)})
    register_expires = ET.SubElement(begin, 'Register_Expires_{}_'.format(ext_common), attrib={'group':'Ext_{}_/Proxy_and_Registration'.format(ext_common)})
    preferred_codec = ET.SubElement(begin, 'Preferred_Codec_{}_'.format(ext_common), attrib={'group':'Ext_{}_/Audio_Configuration'.format(ext_common)})
    use_pref_codec_only = ET.SubElement(begin, 'Use_Pref_Codec_Only_{}_'.format(ext_common), attrib={'group':'Ext_{}_/Audio_Configuration'.format(ext_common)})
    second_preferred_codec = ET.SubElement(begin, 'Second_Preferred_Codec_{}_'.format(ext_common), attrib={'group':'Ext_{}_/Audio_Configuration'.format(ext_common)})
    third_preferred_codec = ET.SubElement(begin, 'Third_Preferred_Codec_{}_'.format(ext_common), attrib={'group':'Ext_{}_/Audio_Configuration'.format(ext_common)})

with open('cisco_inventory.yml', 'r') as inventory:
	output = yaml.load(inventory)
	for device in output:
		for name in output[device]:
			begin = ET.Element('flat-profile')
			begin.insert(0, ET.Comment('Station Configuration'))
			station_name = ET.SubElement(begin, 'Station_Name', attrib={'group':'Phone/General'})
			station_name.text = str(name)
			station_display_name = ET.SubElement(begin, 'Station_Display_Name', attrib={'group':'Phone/General'})
			
			for ext_number in output[device][name]:
				extension(ext_number['extension_number']);
			for options in output[device][name]:
				ext_common(options['extension_number']);
			mydata = minidom.parseString(ET.tostring(begin)).toprettyxml(indent=" ")
			with open("sample{}test.xml".format(name), "w") as myfile:
				myfile.write(mydata)
