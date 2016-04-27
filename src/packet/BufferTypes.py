import struct

boolean = struct.Struct("<?")

uint8 = struct.Struct("<B")
uint16 = struct.Struct("<H")
uint32 = struct.Struct("<I")
uint64 = struct.Struct("<Q")

int8 = struct.Struct("<b")
int16 = struct.Struct("<h")
int24 = struct.Struct("<L")
int32 = struct.Struct("<i")
int64 = struct.Struct("<q")

float32 = struct.Struct("<f")
float64 = struct.Struct("<d")

string = struct.Struct("<s")

uoffset = uint32
soffset = int32
voffset = uint16