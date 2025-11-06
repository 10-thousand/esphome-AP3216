from esphome import automation, pins
import esphome.codegen as cg
from esphome.components import i2c, sensor, binary_sensor, text_sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_AMBIENT_LIGHT,
    CONF_ID,
    CONF_NAME,
    CONF_TRIGGER_ID,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_PRESENCE,
    ICON_BRIGHTNESS_5,
    ICON_BRIGHTNESS_6,
    ICON_MOTION_SENSOR,
    ICON_SCREEN_ROTATION,
    STATE_CLASS_MEASUREMENT,
    UNIT_LUX,
)

DEPENDENCIES = ["i2c"]
AUTO_LOAD = ["sensor", "binary_sensor", "text_sensor"]

REQUIRED_LIBRARIES = [
    "Wire",
]

CONF_INTERRUPT_PIN = "interrupt_pin"

CONF_INFRARED_COUNTS = "infrared_counts"
CONF_PS_COUNTS = "ps_counts"

CONF_IS_NEAR = "is_near"
UNIT_COUNTS = "#"
ICON_PROXIMITY = "mdi:hand-wave-outline"

CONF_MODE="mode"
CONF_OPERATING_MODE = "operating_mode"
CONF_INT_STATUS="interrupt_status"
CONF_IR_DATA="ir_data"

CONF_LUX_RANGE="lux_range"

CONF_ALS_INT_AFTER_N_CONVERSIONS = "als_int_after_n_conversions"
CONF_ALS_CALIBRATION_FACTOR = "als_calibration_factor"
CONF_PS_INTEGRATION_TIME = "ps_integration_time"
CONF_PS_GAIN = "ps_gain"
CONF_PS_INT_AFTER_N_CONVERSIONS = "ps_int_after_n_conversions"
CONF_NUMBER_OF_LED_PULSES = "number_of_led_pulses"
CONF_LED_CURRENT="led_current"
CONF_PS_INTERRUPT_MODE="ps_interrupt_mode"
CONF_PS_MEAN_TIME="ps_mean_time"
CONF_ALS_THRESHOLDS_LOWER = "als_thresholds_lower"
CONF_ALS_THRESHOLDS_UPPER = "als_thresholds_upper"

CONF_PS_THRESHOLDS_LOWER = "ps_thresholds_lower"
CONF_PS_THRESHOLDS_UPPER = "ps_thresholds_upper"

CONF_LED_WAITING_TIME = "led_waiting_time"
CONF_PS_CALIBRATION = "ps_calibration"

CONF_ON_PS_HIGH_THRESHOLD = "on_ps_high_threshold"
CONF_ON_PS_LOW_THRESHOLD = "on_ps_low_threshold"
CONF_ON_IR_DATA_OVERFLOW = "on_ir_data_overflow"
CONF_INT_CLEAR_MANNER = "int_clear_manner"

CONF_ON_INTERRUPT_TRIGGER = "on_interrupt_trigger"

ap3216_ns = cg.esphome_ns.namespace("ap3216")

AP3216Component = ap3216_ns.class_(
    "AP3216Component", cg.PollingComponent, i2c.I2CDevice
)

AP3216Data = ap3216_ns.class_(
    "AP3216Data"
)

AP3216PsHighTrigger = ap3216_ns.class_(
    "AP3216PsHighTrigger", automation.Trigger.template()
)
AP3216PsLowTrigger = ap3216_ns.class_(
    "AP3216PsLowTrigger", automation.Trigger.template()
)

AP3216IrDataIsOverflowedTrigger = ap3216_ns.class_(
    "AP3216IrDataIsOverflowedTrigger", automation.Trigger.template()
)

AP3216InterruptTrigger = ap3216_ns.class_('AP3216InterruptTrigger', automation.Trigger.template())

AP3216MODE = cg.global_ns.enum("AP3216Mode")
AP3216LUX_RANGE = cg.global_ns.enum("AP3216LuxRange")

MODE_OPTIONS = {
    "ALS": AP3216MODE.AP3216_ALS,
    "PS": AP3216MODE.AP3216_PS,
    "ALS_PS": AP3216MODE.AP3216_ALS_PS,
    "RESET": AP3216MODE.AP3216_RESET,
}

OPERATING_MODE_OPTIONS = {
    "VALUE": 0,
    "INTERRUPT": 1,
    "VALUE_AND_INTERRUPT": 2,
}

LUX_RANGE_OPTIONS = {
    "RANGE_20661": AP3216LUX_RANGE.RANGE_20661,
    "RANGE_5162" : AP3216LUX_RANGE.RANGE_5162,
    "RANGE_1291" : AP3216LUX_RANGE.RANGE_1291,
    "RANGE_323"  : AP3216LUX_RANGE.RANGE_323,
}

LED_CURRENT_OPTIONS = {
    "LED_16_7": AP3216MODE.LED_16_7,
    "LED_33_3" : AP3216MODE.LED_33_3,
    "LED_66_7" : AP3216MODE.LED_66_7,
    "LED_100"  : AP3216MODE.LED_100,
}

PS_INTERRUPT_OPTIONS = {
    "INT_MODE_ZONE": AP3216MODE.INT_MODE_ZONE,
    "INT_MODE_HYSTERESIS" : AP3216MODE.INT_MODE_HYSTERESIS,
}

PS_MEAN_TIME_OPTIONS ={
    "PS_MEAN_TIME_12_5": AP3216MODE.PS_MEAN_TIME_12_5,
    "PS_MEAN_TIME_25": AP3216MODE.PS_MEAN_TIME_25,
    "PS_MEAN_TIME_37_5": AP3216MODE.PS_MEAN_TIME_37_5,
    "PS_MEAN_TIME_50": AP3216MODE.PS_MEAN_TIME_50,
}

INT_CLEAR_MANNER_OPTIONS = {
    "CLR_INT_BY_DATA_READ": AP3216MODE.CLR_INT_BY_DATA_READ,
    "CLR_INT_MANUALLY": AP3216MODE.CLR_INT_MANUALLY,
}

def validate_thresholds(config):
    has_als_lower_thresh = CONF_ALS_THRESHOLDS_LOWER in config
    has_als_upper_thresh = CONF_ALS_THRESHOLDS_UPPER in config
    if has_als_lower_thresh != has_als_upper_thresh:
        raise cv.Invalid("als_lower_thresh and als_upper_thresh must be both set or both not set")
        
    if has_als_lower_thresh and has_als_upper_thresh:
        if (has_als_lower_thresh > has_als_upper_thresh):
            raise cv.Invalid("has_als_lower_thresh must be less then has_als_upper_thresh")
        
    has_ps_lower_thresh = CONF_PS_THRESHOLDS_LOWER in config
    has_ps_upper_thresh = CONF_PS_THRESHOLDS_UPPER in config
    if has_ps_lower_thresh != has_ps_upper_thresh:
        raise cv.Invalid("ps_lower_thresh and ps_upper_thresh must be both set or both not set")
    
    if has_ps_lower_thresh and has_ps_upper_thresh:
        if (has_ps_lower_thresh > has_ps_upper_thresh):
            raise cv.Invalid("has_ps_lower_thresh must be less then has_ps_upper_thresh")
    return config


def validate_mode(config):
    operating_mode = config.get(CONF_OPERATING_MODE)
    if operating_mode == "VALUE":
        if CONF_ALS_THRESHOLDS_LOWER in config:
            raise cv.Invalid("Cannot use als_thresholds_lower. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_ALS_THRESHOLDS_UPPER in config:
            raise cv.Invalid("Cannot use als_thresholds_upper. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_PS_THRESHOLDS_LOWER in config:
            raise cv.Invalid("Cannot use ps_thresholds_lower. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_PS_THRESHOLDS_UPPER in config:
            raise cv.Invalid("Cannot use ps_thresholds_upper. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_PS_INTERRUPT_MODE in config:
            raise cv.Invalid("Cannot use ps_interrupt_mode. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_PS_INT_AFTER_N_CONVERSIONS in config:
            raise cv.Invalid("Cannot use ps_int_after_n_conversions. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_ALS_INT_AFTER_N_CONVERSIONS in config:
            raise cv.Invalid("Cannot use als_int_after_n_conversions. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_INTERRUPT_PIN in config:
            raise cv.Invalid("Cannot use interrupt_pin. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
        if CONF_INT_CLEAR_MANNER in config:
            raise cv.Invalid("Cannot use int_clear_manner. Only INTERRUPT and VALUE_AND_INTERRUPT mode support this parameter.")
    return config
    
CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AP3216Component),

            cv.Optional(CONF_INT_STATUS): cv.maybe_simple_value(
                text_sensor.text_sensor_schema(icon=ICON_SCREEN_ROTATION),
                key=CONF_NAME,
            ),
            cv.Optional(CONF_IR_DATA): cv.maybe_simple_value(
                sensor.sensor_schema(
                    icon=ICON_BRIGHTNESS_6,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_ILLUMINANCE,
                ),
                key=CONF_NAME,
            ),
            
             cv.Optional(CONF_PS_COUNTS): cv.maybe_simple_value(
                sensor.sensor_schema(
                    unit_of_measurement=UNIT_COUNTS,
                    icon=ICON_PROXIMITY,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_DISTANCE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                key=CONF_NAME,
            ),
            cv.Optional(CONF_INFRARED_COUNTS): cv.maybe_simple_value(
                sensor.sensor_schema(
                    unit_of_measurement=UNIT_COUNTS,
                    icon=ICON_BRIGHTNESS_5,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_ILLUMINANCE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                key=CONF_NAME,
            ),

            cv.Optional(CONF_AMBIENT_LIGHT): cv.maybe_simple_value(
                sensor.sensor_schema(
                    unit_of_measurement=UNIT_LUX,
                    icon=ICON_BRIGHTNESS_6,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_ILLUMINANCE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                key=CONF_NAME,
            ),
            
            cv.Optional(CONF_IS_NEAR): cv.maybe_simple_value(
                binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PRESENCE,
                    icon=ICON_MOTION_SENSOR,
                ),
                key=CONF_NAME,
            ),
            
            cv.Optional(CONF_ON_PS_HIGH_THRESHOLD): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(AP3216PsHighTrigger),
                }
            ),
            cv.Optional(CONF_ON_PS_LOW_THRESHOLD): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(AP3216PsLowTrigger),
                }
            ),
            
            cv.Optional(CONF_ON_IR_DATA_OVERFLOW): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(AP3216IrDataIsOverflowedTrigger),
                }
            ),
            
            cv.Optional(CONF_ON_INTERRUPT_TRIGGER): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(AP3216InterruptTrigger),

                },
            ),
            
            cv.Optional(CONF_OPERATING_MODE, default="VALUE"): cv.enum(OPERATING_MODE_OPTIONS),
            cv.Optional(CONF_MODE, default="ALS_PS"): cv.enum(MODE_OPTIONS),
            cv.Optional(CONF_INT_CLEAR_MANNER): cv.enum(INT_CLEAR_MANNER_OPTIONS),
            cv.Optional(CONF_LUX_RANGE, default="RANGE_20661"): cv.enum(LUX_RANGE_OPTIONS),
            cv.Optional(CONF_ALS_INT_AFTER_N_CONVERSIONS): cv.int_range(min=1, max=60),
            cv.Optional(CONF_ALS_CALIBRATION_FACTOR, default=1.0): cv.float_range(min=1.0, max=3.98),
            cv.Optional(CONF_PS_INTEGRATION_TIME, default=1): cv.int_range(min=1, max=16),
            cv.Optional(CONF_PS_GAIN, default=2): cv.one_of(1, 2, 4, 8, int=True),
            cv.Optional(CONF_PS_INT_AFTER_N_CONVERSIONS): cv.one_of(1, 2, 4, 8, int=True),
            cv.Optional(CONF_NUMBER_OF_LED_PULSES, default=1): cv.int_range(min=0, max=3),
            cv.Optional(CONF_LED_CURRENT, default="LED_100"): cv.enum(LED_CURRENT_OPTIONS),
            cv.Optional(CONF_PS_INTERRUPT_MODE): cv.enum(PS_INTERRUPT_OPTIONS),
            cv.Optional(CONF_PS_MEAN_TIME, default="PS_MEAN_TIME_12_5"): cv.enum(PS_MEAN_TIME_OPTIONS),
            cv.Optional(CONF_LED_WAITING_TIME, default=0): cv.int_range(min=0, max=63),
            cv.Optional(CONF_PS_CALIBRATION, default=0): cv.int_range(min=0, max=511),
            cv.Optional(CONF_INTERRUPT_PIN): pins.internal_gpio_input_pin_schema,
            cv.Optional(CONF_ALS_THRESHOLDS_LOWER): cv.int_range(min=0),
            cv.Optional(CONF_ALS_THRESHOLDS_UPPER): cv.int_range(min=1),
            cv.Optional(CONF_PS_THRESHOLDS_LOWER): cv.int_range(min=0),
            cv.Optional(CONF_PS_THRESHOLDS_UPPER): cv.int_range(min=1),
        } 
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(i2c.i2c_device_schema(0x23)),
    validate_mode,
    validate_thresholds
           
       
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    cg.add_library("AP3216_WE", None, "https://github.com/wollewald/AP3216_WE.git")
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
    
    if int_status_config := config.get(CONF_INT_STATUS):
        sens = await text_sensor.new_text_sensor(int_status_config)
        cg.add(var.set_interrupt_status_sensor(sens))

    if ir_data_config := config.get(CONF_IR_DATA):
        sens = await sensor.new_sensor(ir_data_config)
        cg.add(var.set_ir_data_sensor(sens))

    if als_config := config.get(CONF_AMBIENT_LIGHT):
        sens = await sensor.new_sensor(als_config)
        cg.add(var.set_ambient_light_sensor(sens))
        
    if prox_cnt_config := config.get(CONF_PS_COUNTS):
        sens = await sensor.new_sensor(prox_cnt_config)
        cg.add(var.set_proximity_counts_sensor(sens))
        
    if infrared_cnt_config := config.get(CONF_INFRARED_COUNTS):
        sens = await sensor.new_sensor(infrared_cnt_config)
        cg.add(var.set_infrared_counts_sensor(sens))
        
    if is_near_config := config.get(CONF_IS_NEAR):
        sens = await binary_sensor.new_binary_sensor(is_near_config)
        cg.add(var.set_is_near_sensor(sens))
    
    for prox_high_tr in config.get(CONF_ON_PS_HIGH_THRESHOLD, []):
        trigger = cg.new_Pvariable(prox_high_tr[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], prox_high_tr)

    for prox_low_tr in config.get(CONF_ON_PS_LOW_THRESHOLD, []):
        trigger = cg.new_Pvariable(prox_low_tr[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], prox_low_tr)
        
    for ir_data_overflow in config.get(CONF_ON_IR_DATA_OVERFLOW, []):
        trigger = cg.new_Pvariable(ir_data_overflow[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], ir_data_overflow)
    
    cg.add(var.set_operating_mode(config[CONF_OPERATING_MODE]))    
    cg.add(var.set_mode(config[CONF_MODE]))
    if CONF_INT_CLEAR_MANNER in config:
        cg.add(var.set_int_clear_manner(config[CONF_INT_CLEAR_MANNER]))
    if CONF_ALS_INT_AFTER_N_CONVERSIONS in config:
        cg.add(var.set_als_int_after_n_conversions(config[CONF_ALS_INT_AFTER_N_CONVERSIONS]))
    if CONF_PS_INT_AFTER_N_CONVERSIONS in config:
        cg.add(var.set_ps_int_after_n_conversions(config[CONF_PS_INT_AFTER_N_CONVERSIONS]))
    if CONF_PS_INTERRUPT_MODE in config:
        cg.add(var.set_ps_interrupt_mode(config[CONF_PS_INTERRUPT_MODE]))
        
    cg.add(var.set_lux_range(config[CONF_LUX_RANGE]))
    cg.add(var.set_als_calibration_factor(config[CONF_ALS_CALIBRATION_FACTOR]))
    cg.add(var.set_ps_integration_time(config[CONF_PS_INTEGRATION_TIME]))
    cg.add(var.set_ps_gain(config[CONF_PS_GAIN]))
    
    cg.add(var.set_number_of_led_pulses(config[CONF_NUMBER_OF_LED_PULSES]))
    cg.add(var.set_led_current(config[CONF_LED_CURRENT]))
    
    cg.add(var.set_ps_mean_time(config[CONF_PS_MEAN_TIME]))
    cg.add(var.set_led_waiting_time(config[CONF_LED_WAITING_TIME]))
    cg.add(var.set_ps_calibration(config[CONF_PS_CALIBRATION]))
    
    if CONF_ALS_THRESHOLDS_LOWER in config and CONF_ALS_THRESHOLDS_UPPER in config:
        cg.add(var.set_als_thresholds(config[CONF_ALS_THRESHOLDS_LOWER], config[CONF_ALS_THRESHOLDS_UPPER]))
    
    if CONF_PS_THRESHOLDS_LOWER in config and CONF_PS_THRESHOLDS_UPPER in config:
        cg.add(var.set_ps_thresholds(config[CONF_PS_THRESHOLDS_LOWER], config[CONF_PS_THRESHOLDS_UPPER]))
    if CONF_INTERRUPT_PIN in config:
        interrupt_pin = await cg.gpio_pin_expression(config[CONF_INTERRUPT_PIN])
        cg.add(var.set_interrupt_pin(interrupt_pin))
    
    for conf in config.get(CONF_ON_INTERRUPT_TRIGGER, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(
                trigger, [(AP3216Data.operator("ref"), "x")],
                
                conf,
            ) 

        