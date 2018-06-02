import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml.components import sensor
from esphomeyaml.const import CONF_HUMIDITY, CONF_MAKE_ID, CONF_NAME, CONF_TEMPERATURE, \
    CONF_UPDATE_INTERVAL
from esphomeyaml.helpers import App, variable, Application

DEPENDENCIES = ['i2c']

MakeHTU21DSensor = Application.MakeHTU21DSensor

PLATFORM_SCHEMA = sensor.PLATFORM_SCHEMA.extend({
    cv.GenerateID(CONF_MAKE_ID): cv.declare_variable_id(MakeHTU21DSensor),
    vol.Required(CONF_TEMPERATURE): sensor.SENSOR_SCHEMA,
    vol.Required(CONF_HUMIDITY): sensor.SENSOR_SCHEMA,
    vol.Optional(CONF_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
})


def to_code(config):
    rhs = App.make_htu21d_sensor(config[CONF_TEMPERATURE][CONF_NAME],
                                 config[CONF_HUMIDITY][CONF_NAME],
                                 config.get(CONF_UPDATE_INTERVAL))
    htu21d = variable(config[CONF_MAKE_ID], rhs)
    for _ in sensor.setup_sensor(htu21d.Phtu21d.Pget_temperature_sensor(), htu21d.Pmqtt_temperature,
                                 config[CONF_TEMPERATURE]):
        yield
    for _ in sensor.setup_sensor(htu21d.Phtu21d.Pget_humidity_sensor(), htu21d.Pmqtt_humidity,
                                 config[CONF_HUMIDITY]):
        yield


BUILD_FLAGS = '-DUSE_HTU21D_SENSOR'
