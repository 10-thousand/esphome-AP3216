# ESPHome custom component for СJMCU-3216 (AP3216)
## 1. Connect AP3216 to a board (image for example)
   
![](https://github.com/10-thousand/esphome-AP3216/blob/main/scheme.jpg)

## 2. Include the external component in the yaml file:
```
external_components:
  - source: github://10-thousand/esphome-AP3216@main
    components: [ap3216]
```
## 3. Use AP3216 sensor
```
i2c:
  sda: GPIO21
  scl: GPIO22
  
sensor:
  - platform: ap3216
    mode: ALS_PS
    operating_mode: VALUE
    ambient_light: "Ambient light"
    ps_counts: "Proximity"
    infrared_counts: "Infrared"
    ir_data: "Ir data"
    is_near: "is_near"
    
    address: 0x23
    update_interval: 60s
```    
You can see [minimal](https://github.com/10-thousand/esphome-AP3216/blob/main/minimal_example_ap3216.yaml) and [full](https://github.com/10-thousand/esphome-AP3216/blob/main/example_ap3216.yaml) example in this repo

This project uses the [AP3216_WE](https://github.com/wollewald/AP3216_WE/tree/master) library.
