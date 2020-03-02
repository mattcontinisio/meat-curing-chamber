import 'dart:async';

import 'package:flutter/material.dart';

import 'package:mqtt_client/mqtt_server_client.dart';
import 'package:mqtt_client/mqtt_client.dart';

class SensorDisplay extends StatefulWidget {
  SensorDisplay({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _SensorDisplayState createState() => _SensorDisplayState();
}

class _SensorDisplayState extends State<SensorDisplay> {
  String _selectedLocation = 'home/bedroom';
  final _locations = {
    'home/bedroom': {'humidity': 0.0, 'temperature': 0.0},
    'home/living_room': {'humidity': 0.0, 'temperature': 0.0},
    'home/kitchen/fridge': {'humidity': 0.0, 'temperature': 0.0}
  };

  MqttServerClient _client;
  StreamSubscription _subscription;

  void _connect() async {
    debugPrint('connecting');
    String broker = '192.168.1.115';
    String clientId = 'monitor_flutter';
    int port = 1883;
    _client = MqttServerClient.withPort(broker, clientId, port);
    _client.logging(on: true);
    await _client.connect();
    debugPrint('connected, subscribing');

    _subscription = _client.updates.listen(_onMessage);
    final topic = 'home/#';
    _client.subscribe(topic, MqttQos.atLeastOnce);
  }

  void _onMessage(List<MqttReceivedMessage> event) {
    debugPrint('got message');
    final topic = event[0].topic;
    final topicParts = topic.split('/');
    final location = topicParts.sublist(0, topicParts.length - 1).join('/');
    if (!_locations.containsKey(location)) {
      debugPrint('Unknown location: $location');
      return;
    }

    final publishMessage = event[0].payload as MqttPublishMessage;
    final message = MqttPublishPayload.bytesToStringAsString(
        publishMessage.payload.message);

    final humidityOrTemperature = topicParts[topicParts.length - 1];
    if (humidityOrTemperature == 'humidity') {
      setState(() {
        _locations[location]['humidity'] = double.parse(message);
      });
    } else if (humidityOrTemperature == 'temperature') {
      _locations[location]['temperature'] = double.parse(message);
    } else {
      debugPrint('Unexpected value: $humidityOrTemperature');
    }
  }

  @override
  void initState() {
    super.initState();
    _connect();
  }

  @override
  Widget build(BuildContext context) {
    final humidity =
        _locations[_selectedLocation]['humidity'].toStringAsFixed(2);
    final temperature =
        _locations[_selectedLocation]['temperature'].toStringAsFixed(2);

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            DropdownButton<String>(
              value: _selectedLocation,
              onChanged: (String newSelectedLocation) {
                setState(() {
                  _selectedLocation = newSelectedLocation;
                });
              },
              items: ['home/bedroom', 'home/living_room', 'home/kitchen/fridge']
                  .map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
            ),
            Text(
              'humidity:',
            ),
            Text(
              '$humidity',
              style: Theme.of(context).textTheme.display1,
            ),
            Text(
              'temperature:',
            ),
            Text(
              '$temperature',
              style: Theme.of(context).textTheme.display1,
            ),
          ],
        ),
      ),
    );
  }
}
