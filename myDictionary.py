MsgTypeDict = {
		'set_Ringtone':0x0F02,
		'get_Product_name':0x9afe,
		'state_changed':0x0200}

PKT_STRUCTURE = [
					("BOOLEAN",0x0200),
					("BYTE",0x0402),
					("STRING",0x1A23),
					("USHORT",0x0A02),
					("BYTE-BYTE",0x0F02),
					("SHORT",0x0052),
					("INT",0x0053),
					("LONG",0x0054),
					("BYTE_ARRAY",0x0057)
					]