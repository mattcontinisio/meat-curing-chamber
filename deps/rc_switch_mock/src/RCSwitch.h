#pragma once

#include <stdint.h>

class RCSwitch {
    void sendTriState(const char* sCodeWord) {}
    void send(unsigned long code, unsigned int length) {}
    void send(const char* sCodeWord) {}

    #if not defined( RCSwitchDisableReceiving )
    void enableReceive(int interrupt) {}
    void enableReceive() {}
    void disableReceive() {}
    bool available() { return true; }
    void resetAvailable() {}

    unsigned long getReceivedValue() { return 0; }
    unsigned int getReceivedBitlength() { return 0; }
    unsigned int getReceivedDelay() { return 0; }
    unsigned int getReceivedProtocol() { return 0; }
    unsigned int* getReceivedRawdata() { return 0; }
    #endif

    void enableTransmit(int nTransmitterPin) {}
    void disableTransmit() {}
    void setPulseLength(int nPulseLength) {}
    void setRepeatTransmit(int nRepeatTransmit) {}
    #if not defined( RCSwitchDisableReceiving )
    void setReceiveTolerance(int nPercent) {}
    #endif

    struct HighLow {
        uint8_t high;
        uint8_t low;
    };

    struct Protocol {
        uint16_t pulseLength;

        HighLow syncFactor;
        HighLow zero;
        HighLow one;

        bool invertedSignal;
    };

    void setProtocol(Protocol protocol) {}
    void setProtocol(int nProtocol) {}
    void setProtocol(int nProtocol, int nPulseLength) {}
};
