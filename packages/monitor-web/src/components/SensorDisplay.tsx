import React, { Component } from 'react';

import mqtt from 'mqtt';

const brokerAddress = 'ws://192.168.1.115:9001'
const location = 'home/kitchen/fridge';

interface SensorDisplayState {
  humidity: number;
  temperature: number;
}

export default class SensorDisplay extends Component<{}, SensorDisplayState> {
  private client: mqtt.MqttClient;

  constructor(props: {}, context?: any) {
    super(props, context);
    this.state = {
      humidity: 0,
      temperature: 0,
    };

    this.client = mqtt.connect(brokerAddress);
    this.client.on('connect', () => {
      const topic = [location, '#'].join('/');
      console.log('subscribing', { topic });
      this.client.subscribe(topic, (err) => {
        if (err) {
          console.error('failed to subscribe', err)
        }
      });

      this.client.on('message', (topic, message) => {
        console.log('got message', topic, message.toString());
        if (topic === [location, 'humidity'].join('/')) {
          this.setState({ humidity: +message.toString() });
        } else if (topic === [location, 'temperature'].join('/')) {
          this.setState({ temperature: +message.toString() });
        } else {
          console.warn('Unexpected topic', topic);
        }
      });
    })
  }

  render() {
    return (
      <div className="SensorDisplay">
        <p>humidity: {+this.state.humidity.toFixed(2)}</p>
        <p>temperature: {+this.state.temperature.toFixed(2)}</p>
      </div>
    );
  }
}
