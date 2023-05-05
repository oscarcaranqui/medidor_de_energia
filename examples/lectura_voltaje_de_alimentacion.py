
from dispositivos_i2c.MCP3424 import MCP3424, SampleRate, ChannelSelection, PGA

BITBANG = True

if not BITBANG:
    from bsp.v3.i2c_generic import AddressI2Chw

    # creating i2c hw address object
    # you can use channel 0 or channel 1
    # i2cdetect -y 0 -> channel 0
    # i2cdetect -y 1 -> channel 1
    # channel 3 for orange pi zero 2
    address = AddressI2Chw(
        aplicacion='adc',
        channel=0,
        address=0x6f
    )

else:
    from bsp.v3.i2c_generic import AddressI2Cbb

    # creating i2c bb address object
    address = AddressI2Cbb(
        aplicacion='adc',
        scl_pin=28,  # gpio 1
        sda_pin=27,  # gpio 0
        address=0x6f
    )

# creating adc mcp3424 object
# battery is measured in adc channel 2
# 4-20ma port 1 -> ChannelSelection.channel_4
adc = MCP3424(
    address=address,
    sample_rate=SampleRate.sr_18bits_3_75sps,
    channel=ChannelSelection.channel_2,
    pga=PGA.x1
)

# printing adc value
print('v_batt: %f' % (adc.value_v * (100 + 10) / 10))
