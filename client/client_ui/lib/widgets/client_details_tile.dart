import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';

class ClientDetailsTile extends StatelessWidget {
  final String clientId;
  final String name;
  final String status;
  const ClientDetailsTile({super.key, required this.clientId, required this.name, required this.status});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Row(children: [const Text("Name:", style: TextStyle(fontWeight: FontWeight.bold),), const SizedBox(width: 10,), Text(name)],),
        subtitle: Column(
          children: [
            Row(children: [const Text("Client Id:", style: TextStyle(fontWeight: FontWeight.bold),), const SizedBox(width: 10,), Text(clientId)],),
            Row(children: [const Text("Status:", style: TextStyle(fontWeight: FontWeight.bold),), const SizedBox(width: 10,), Text(status)],)
          ],
        ),
        trailing: SelectionContainer.disabled(child: ElevatedButton(child: Text("Connect"), onPressed: (){})),
      ),
    );
  }
}