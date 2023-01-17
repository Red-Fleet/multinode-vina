import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/user_model.dart';
import 'package:ui/widgets/homepage.dart';
import 'package:ui/widgets/login_register.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Multinode Vina"),
        backgroundColor: Colors.black,
      ),
      body: Provider.of<UserModel>(context, listen: true).isAuthenticated==true? const HomePage(): const LoginRegister()
    );
  }
}