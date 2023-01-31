import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';

class ConnectedClients extends StatefulWidget {
  const ConnectedClients({super.key});

  @override
  State<ConnectedClients> createState() => _ConnectedClientsState();
}

class _ConnectedClientsState extends State<ConnectedClients> {
  
  @override
  Widget build(BuildContext context) {
    return FutureBuilder(builder: (context, snapshot){
      if(snapshot.hasData){
        return Container();
      }
      else{
        return const CircularProgressIndicator();
      }
    });
  }
}