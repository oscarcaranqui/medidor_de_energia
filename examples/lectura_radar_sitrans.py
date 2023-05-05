
import pprint

from bsp.common.util import asdict_without_datetostr
from bsp.common.PlatformDetector import GPIO
from bsp.v3.i2c_generic import AddressI2Chw
from dispositivos_i2c.MCP3424 import MCP3424, SampleRate, ChannelSelection, PGA
from dispositivos_i2c.SITRANSRadar import RadarCombustible

# creating i2c hw address object
# you can use channel 0 or channel 1
# i2cdetect -y 0 -> channel 0
# i2cdetect -y 1 -> channel 1
address = AddressI2Chw(
    aplicacion='adc',
    channel=0,
    address=0x6f
)

# creating adc mcp3424 object
# you can use adc channel 1 or 4
# 4-20ma port 1 -> ChannelSelection.channel_4
# 4-20ma port 2 -> ChannelSelection.channel_1
adc = MCP3424(
    address=address,
    sample_rate=SampleRate.sr_18bits_3_75sps,
    channel=ChannelSelection.channel_1,
    pga=PGA.x1
)

# initialiting gpio 7 in order to turn on 12v pin of 4-20ma port 1 and 2
# gpio high turn on 12v
# gpio low turn off 12v
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)

# initialiting radar object
cal_inf = 2.03
cal_sup = 0.13
radar = RadarCombustible(adc=adc, id=None, cal_inf=cal_inf, cal_sup=cal_sup)

# printing result
pprint.pprint(asdict_without_datetostr(radar))
