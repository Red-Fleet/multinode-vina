import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/server_model.dart';
import 'package:ui/models/user_model.dart';
import 'package:ui/widgets/homepage.dart';

void main() {
  runApp(const MaterialApp(
    title: "Multinode Vina",
    home: MultiNodeVina(),
  ));
}

class MultiNodeVina extends StatefulWidget {
  const MultiNodeVina({super.key});

  @override
  State<MultiNodeVina> createState() => _MultiNodeVinaState();
}

class _MultiNodeVinaState extends State<MultiNodeVina> {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => ServerModel()),
        ChangeNotifierProvider(create: (context) => UserModel())
      ],
      child: const HomePage(),
    );
  }
}
