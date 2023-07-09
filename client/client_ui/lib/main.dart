import 'package:flutter/material.dart';
import 'package:flutter_web_plugins/url_strategy.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/user_model.dart';
import 'package:ui/screens/main_screen.dart';

void main() {
  usePathUrlStrategy();
  runApp(const MaterialApp(
    title: "Multinode Vina",
    home: MultiNodeVina(),
    debugShowCheckedModeBanner: false,
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
        ChangeNotifierProvider(create: (context) => UserModel())
      ],
      child: const MainScreen(),
    );
  }
}
