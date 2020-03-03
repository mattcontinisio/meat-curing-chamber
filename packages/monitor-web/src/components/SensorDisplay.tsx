import React, { Component } from 'react';

import mqtt from 'mqtt';

const brokerAddress = 'ws://192.168.1.115:9001';

interface SensorDisplayState {
  selectedLocation: string; // 'home/bedroom' | 'home/living_room' | 'home/kitchen/fridge'
  locations: {
    [key: string]: {
      humidity: number;
      temperature: number;
    };
  };
}

export default class SensorDisplay extends Component<{}, SensorDisplayState> {
  private client: mqtt.MqttClient;

  constructor(props: {}, context?: any) {
    super(props, context);
    this.state = {
      selectedLocation: 'home/bedroom',
      locations: {
        'home/bedroom': {
          humidity: 0,
          temperature: 0
        },
        'home/living_room': {
          humidity: 0,
          temperature: 0
        },
        'home/kitchen/fridge': {
          humidity: 0,
          temperature: 0
        }
      }
    };

    this.client = mqtt.connect(brokerAddress);
    this.client.on('connect', () => {
      const topic = ['home', '#'].join('/');
      console.log('subscribing', { topic });
      this.client.subscribe(topic, err => {
        if (err) {
          console.error('failed to subscribe', err);
        }
      });

      this.client.on('message', (topic, message) => {
        console.log('got message', topic, message.toString());
        const topicParts = topic.split('/');
        const location = topicParts.slice(0, -1).join('/');
        if (!(location in this.state.locations)) {
          console.warn('Unknown location', location);
          return;
        }

        const humidityOrTemperature = topicParts[topicParts.length - 1];
        if (humidityOrTemperature === 'humidity') {
          this.setState(state => {
            state.locations[location].humidity = +message.toString();
            return state;
          });
        } else if (humidityOrTemperature === 'temperature') {
          this.setState(state => {
            state.locations[location].temperature = +message.toString();
            return state;
          });
        } else {
          console.warn('Unexpected');
        }
      });
    });
  }

  handleChangeLocation(event: React.ChangeEvent<HTMLSelectElement>) {
    this.setState({ selectedLocation: event.target.value });
  }

  render() {
    const locationData = this.state.locations[this.state.selectedLocation];
    const humidity = `humidity: ${locationData.humidity.toFixed(2)} %`;
    const temperature = `temperature: ${locationData.temperature.toFixed(2)} °C`;

    return (
      <div className="SensorDisplay">
        <label>
          location
          <select
            value={this.state.selectedLocation}
            onChange={this.handleChangeLocation.bind(this)}
          >
            <option value="home/bedroom">home/bedroom</option>
            <option value="home/living_room">home/living_room</option>
            <option value="home/kitchen/fridge">home/kitchen/fridge</option>
          </select>
        </label>
        <p>{humidity}</p>
        <p>{temperature}</p>
      </div>
    );
  }
}
