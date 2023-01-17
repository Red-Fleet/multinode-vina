import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/user_model.dart';
import 'package:ui/widgets/login_register.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Text("logined");
  }
}