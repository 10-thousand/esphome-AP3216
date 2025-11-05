#include "ap3216.h"
#include "Wire.h"
#include "esphome/core/log.h"

namespace esphome {
namespace ap3216 {
    
    volatile bool event = false;
    
    static const char *const TAG = "ap3216.sensor";
    
    AP3216_WE _AP3216 = AP3216_WE();
    
    void AP3216Component::setup(){
      
      _AP3216.init();

      if (operating_mode == 1 || operating_mode == 2){
          int pin = interrupt_pin_->get_pin();
          pinMode(pin, INPUT);
          attachInterrupt(digitalPinToInterrupt(pin), blink, CHANGE); 
          _AP3216.setALSThresholds(als_lower_thresh, als_upper_thresh);
          _AP3216.setPSThresholds(ps_lower_thresh, ps_upper_thresh); 
          _AP3216.setPSInterruptMode(ps_interrupt_mode);
          _AP3216.setPSIntAfterNConversions(ps_int_after_n_conversions);
          _AP3216.setALSIntAfterNConversions(als_int_after_n_conversions);  
          _AP3216.setIntClearManner(int_clear_manner);  
      }
      
     
      _AP3216.setMode(_ap3216_mode);
      _AP3216.setLuxRange(lux_range);   
      
     
      _AP3216.setALSCalibrationFactor(als_calibration_factor);
      _AP3216.setPSIntegrationTime(ps_integration_time);  
      
      _AP3216.setPSGain(ps_gain);
      
      _AP3216.setNumberOfLEDPulses(number_of_led_pulses);
      _AP3216.setLEDCurrent(led_current);
     
      _AP3216.setPSMeanTime(ps_mean_time);
      _AP3216.setLEDWaitingTime(led_waiting_time);
      _AP3216.setPSCalibration(ps_calibration);
    
    
      
      delay(1000);
    }
    
    void AP3216Component::dump_config() {
      
      
      ESP_LOGCONFIG(TAG, "_AP3216 init");
      
      if (operating_mode == 1 || operating_mode == 2){
          ESP_LOGCONFIG(TAG, "ALSThresholds: %d-%d", this->als_lower_thresh, this->als_upper_thresh);
          ESP_LOGCONFIG(TAG, "PSThresholds: %d-%d", this->ps_lower_thresh, this->ps_upper_thresh);
          ESP_LOGCONFIG(TAG, "ps_interrupt_mode: %d", this->ps_interrupt_mode);
          ESP_LOGCONFIG(TAG, "ps_int_after_n_conversions: %d ", this->ps_int_after_n_conversions);
          ESP_LOGCONFIG(TAG, "als_int_after_n_conversions: %d ", this->als_int_after_n_conversions);
          ESP_LOGCONFIG(TAG, "int_clear_manner: %d ", this->int_clear_manner);
      }

      ESP_LOGCONFIG(TAG, "operating_mode: %d ", this->operating_mode);
      ESP_LOGCONFIG(TAG, "mode: %d ", this->_ap3216_mode);
      ESP_LOGCONFIG(TAG, "lux_range: %d ", this->lux_range);
      ESP_LOGCONFIG(TAG, "als_calibration_factor: %f ", this->als_calibration_factor);
      ESP_LOGCONFIG(TAG, "ps_integration_time: %d ", this->ps_integration_time);

      ESP_LOGCONFIG(TAG, "ps_gain: %d ", this->ps_gain);
      ESP_LOGCONFIG(TAG, "number_of_led_pulses: %d ", this->number_of_led_pulses);
      ESP_LOGCONFIG(TAG, "led_current: %d ", this->led_current);
      
      ESP_LOGCONFIG(TAG, "ps_mean_time: %d ", this->ps_mean_time);
      ESP_LOGCONFIG(TAG, "led_waiting_time: %d ", this->led_waiting_time);
      ESP_LOGCONFIG(TAG, "ps_calibration: %d ", this->ps_calibration);
    }
    
    void AP3216Component::interruptAction(){
        
      ESP_LOGI(TAG, "interruptAction ... OK!");
      uint8_t  intType = NO_INT;
      intType = _AP3216.getIntStatus();
      AP3216Data data;
      data.interruptType = intType;
      switch(intType){
        case(ALS_INT):
           ESP_LOGI(TAG, "Ambient Light Interrupt!"); 
           data.interruptTypeString = "ALS_INT";
           data.als = _AP3216.getAmbientLight();
           data.prox = _AP3216.getProximity();
           data.ir = _AP3216.getIRData();
           this->on_interrupt_callback_.call(data);
          break;
        case(PS_INT):
           data.interruptTypeString = "PS_INT";
           ESP_LOGI(TAG, "Proximity Interrupt!");
           data.als = _AP3216.getAmbientLight();
           data.prox = _AP3216.getProximity();
           data.ir = _AP3216.getIRData();
           this->on_interrupt_callback_.call(data);
          break;
        case(ALS_PS_INT):
           ESP_LOGI(TAG, "Ambient Light and Proximity Interrupt!");
           data.interruptTypeString = "ALS_PS_INT";
           data.als = _AP3216.getAmbientLight();
           data.prox = _AP3216.getProximity();
           data.ir = _AP3216.getIRData();
           this->on_interrupt_callback_.call(data);
          break;
        default:
           ESP_LOGI(TAG, "Something went wrong...");
          break;      
      }
      
     
      
      intType = _AP3216.getIntStatus();
      _AP3216.clearInterrupt(intType);
      event = false;
    }
    
    void AP3216Component::loop(){
        if(event){
            interruptAction();
        }
          /*
           * without the following delay you will not detect ALS and PS interrupts together. 
           */
        delay(1000); 
    }
    void AP3216Component::update() {
      if (operating_mode == 1){
          return;
      }
      float als = _AP3216.getAmbientLight();
      unsigned int prox = _AP3216.getProximity();
      unsigned int intStatus = _AP3216.getIntStatus();
      unsigned int ir = _AP3216.getIRData(); // Ambient IR light
      bool isNear = _AP3216.objectIsNear();
      bool irIsValid = !_AP3216.irDataIsOverflowed();
      if (this->ambient_light_sensor_ != nullptr) {
        this->ambient_light_sensor_->publish_state(als);
      }
      if (this->proximity_counts_sensor_ != nullptr) {
        this->proximity_counts_sensor_->publish_state(prox);
      }
      if (this->infrared_counts_sensor_ != nullptr) {
        this->infrared_counts_sensor_->publish_state(ir);
      }
      
      if (isNear){
        this->on_ps_high_trigger_callback_.call();  
      }else{
        this->on_ps_low_trigger_callback_.call();   
      }
      
      if (_AP3216.irDataIsOverflowed()){
         this->on_ir_data_is_overflowed_callback_.call();
      }
      
      if (this->is_near_sensor_ != nullptr){
          this->is_near_sensor_->publish_state(isNear);
      }

      if (this->ir_data_sensor_ != nullptr){
          this->ir_data_sensor_->publish_state(_AP3216.getIRData());
      }
      if (this->interrupt_status_sensor_ != nullptr){
          switch (intStatus)
          {
          case 0:
            this->interrupt_status_sensor_->publish_state("NO_INT");
            break;
            case 1:
            this->interrupt_status_sensor_->publish_state("ALS_INT");
            break;
            case 2:
            this->interrupt_status_sensor_->publish_state("PS_INT");
            break;
            case 3:
            this->interrupt_status_sensor_->publish_state("ALS_PS_INT");
            break;
          }
          
      }
    }
    
    void  AP3216Component::blink(){
      event = true;
    }
}
}