#pragma once

#include "esphome/core/automation.h"
#include "ap3216.h"

namespace esphome {
namespace ap3216 {

    
    class AP3216PsHighTrigger : public Trigger<> {
    friend class AP3216Component;
        public:
            explicit AP3216PsHighTrigger(AP3216Component *parent) {
                parent->add_on_ps_high_trigger_callback_([this]() { this->trigger(); });
            }
    };
    
    class AP3216PsLowTrigger : public Trigger<> {
        public:
            explicit AP3216PsLowTrigger(AP3216Component *parent) {
                parent->add_on_ps_low_trigger_callback_([this]() { this->trigger(); });
            }
    };
    
    class AP3216IrDataIsOverflowedTrigger : public Trigger<> {
        public:
            explicit AP3216IrDataIsOverflowedTrigger(AP3216Component *parent) {
                parent->add_on_ir_data_is_overflowed_callback_([this]() { this->trigger(); });
            }
    };
    
    class AP3216InterruptTrigger : public Trigger<AP3216Data&>
    {
        friend class AP3216Component;
        public:
            explicit AP3216InterruptTrigger(AP3216Component *parent)
            {
                parent->add_on_interrupt_callback_([this](AP3216Data &x) { this->trigger(x); });
            }
   };

}  // namespace ap3216
}  // namespace esphome