#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/i2c/i2c.h"
#include "AP3216_WE.h"
#include "esphome/core/gpio.h"

namespace esphome {
namespace ap3216 {

struct AP3216Data{
  float als;
  unsigned int prox;
  unsigned int ir;
  uint8_t interruptType;
  std::string interruptTypeString;
};
class AP3216Component : public PollingComponent, public i2c::I2CDevice {
 public:
  void setup() override;
  void dump_config() override;
  void update() override;
  void loop() override;
  
  
  void set_interrupt_status_sensor(text_sensor::TextSensor *sensor) { this->interrupt_status_sensor_ = sensor; }
  void set_ambient_light_sensor(sensor::Sensor *sensor) { this->ambient_light_sensor_ = sensor; }
  void set_proximity_counts_sensor(sensor::Sensor *sensor) { this->proximity_counts_sensor_ = sensor; }
  void set_infrared_counts_sensor(sensor::Sensor *sensor) { this->infrared_counts_sensor_ = sensor; }
  void set_is_near_sensor(binary_sensor::BinarySensor *sensor) { this->is_near_sensor_ = sensor; }
  void set_ir_data_sensor(sensor::Sensor *sensor) { this->ir_data_sensor_ = sensor; }
  void set_interrupt_pin(InternalGPIOPin *pin) { interrupt_pin_ = pin; }
  
  void set_operating_mode(uint8_t operating_mode) { this->operating_mode = operating_mode; } 
  void set_mode(AP3216Mode _ap3216_mode) { this->_ap3216_mode = _ap3216_mode; } 
  void set_int_clear_manner(uint8_t int_clear_manner) {this->int_clear_manner = int_clear_manner;}
  void set_lux_range(AP3216LuxRange _ap3216_lux_range) { this->lux_range = _ap3216_lux_range; }
  void set_als_int_after_n_conversions(int number) { this->als_int_after_n_conversions = number; }
  void set_als_calibration_factor(float als_calibration_factor){ this->als_calibration_factor = als_calibration_factor; }
  void set_ps_integration_time(int ps_integration_time){this->ps_integration_time = ps_integration_time;}
  void set_ps_gain(int ps_gain) {this->ps_gain = ps_gain;}
  void set_ps_int_after_n_conversions(int ps_int_after_n_conversions){this->ps_int_after_n_conversions = ps_int_after_n_conversions;}
  void set_number_of_led_pulses(int number_of_led_pulses){this->number_of_led_pulses = number_of_led_pulses;}
  void set_led_current(uint8_t led_current){this->led_current = led_current;}
  void set_ps_interrupt_mode(uint8_t ps_interrupt_mode){this->ps_interrupt_mode = ps_interrupt_mode;}
  void set_ps_mean_time(uint8_t ps_mean_time){this->ps_mean_time = ps_mean_time;}
  void set_led_waiting_time(int led_waiting_time){this->led_waiting_time = led_waiting_time; }
  void set_ps_calibration(int ps_calibration) {this->ps_calibration = ps_calibration;}
  void set_als_thresholds(int lower_thresh, int upper_thresh) {this->als_lower_thresh = lower_thresh; this->als_upper_thresh = upper_thresh;}
  void set_ps_thresholds(int lower_thresh, int upper_thresh) {this->ps_lower_thresh = lower_thresh; this->ps_upper_thresh = upper_thresh;}
  
  CallbackManager<void()> on_ps_high_trigger_callback_;
  CallbackManager<void()> on_ps_low_trigger_callback_;
  CallbackManager<void()> on_ir_data_is_overflowed_callback_;
  CallbackManager<void(AP3216Data &)> on_interrupt_callback_;

  void add_on_ps_high_trigger_callback_(std::function<void()> callback) {
    this->on_ps_high_trigger_callback_.add(std::move(callback));
  }

  void add_on_ps_low_trigger_callback_(std::function<void()> callback) {
    this->on_ps_low_trigger_callback_.add(std::move(callback));
  }
  
  void add_on_ir_data_is_overflowed_callback_(std::function<void()> callback) {
    this->on_ir_data_is_overflowed_callback_.add(std::move(callback));
  }

  void add_on_interrupt_callback_(std::function<void(AP3216Data &)> &&callback){
    this->on_interrupt_callback_.add(std::move(callback));
  }
protected:
  
  sensor::Sensor *ambient_light_sensor_{nullptr}; 
  sensor::Sensor *proximity_counts_sensor_{nullptr};
  sensor::Sensor *infrared_counts_sensor_{nullptr};   
  binary_sensor::BinarySensor *is_near_sensor_{nullptr}; 
  text_sensor::TextSensor *interrupt_status_sensor_{nullptr}; 
  sensor::Sensor *ir_data_sensor_{nullptr}; 
  
  
  uint8_t operating_mode;
  AP3216Mode _ap3216_mode;
  uint8_t int_clear_manner = CLR_INT_BY_DATA_READ;
  AP3216LuxRange lux_range;
  uint8_t als_int_after_n_conversions = 1;
  float als_calibration_factor;
  uint8_t ps_integration_time;
  uint8_t ps_gain;
  uint8_t ps_int_after_n_conversions = 2;
  uint8_t number_of_led_pulses;
  uint8_t led_current;
  uint8_t ps_interrupt_mode = INT_MODE_ZONE;
  uint8_t ps_mean_time;
  uint8_t led_waiting_time;
  uint16_t ps_calibration;
  InternalGPIOPin *interrupt_pin_{nullptr};
  uint16_t als_lower_thresh;
  uint16_t als_upper_thresh;
  uint16_t ps_lower_thresh;
  uint16_t ps_upper_thresh;
  
  static void blink();
  void interruptAction();


}  // namespace ap3216
}  // namespace esphome