import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/user_model.dart';
import 'package:ui/services/client_http_service.dart';
import 'package:ui/widgets/homepage.dart';
import 'package:ui/widgets/login_register.dart';
import 'package:ui/widgets/user_avatar.dart';
import 'dart:convert';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {

  void initUser() async{
    try{
      final userModel = Provider.of<UserModel>(context, listen: false);
      final response = await ClientHttpService.getUserDetails();

      if(response.statusCode == 200){
        final userDetails = jsonDecode(response.body);
        userModel.username = userDetails['username'];
        userModel.name = userDetails['name'];
        userModel.clientId = userDetails['client_id'];
        userModel.password = userDetails['password'];
        userModel.isAuthenticated = true;
      }
    }
    catch(e){
      debugPrint(e.toString());
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    initUser();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Multinode Vina"),
        backgroundColor: Colors.black,
        actions: Provider.of<UserModel>(context, listen: true).isAuthenticated==true?[const UserAvatar()]:[],
      ),
      body: Provider.of<UserModel>(context, listen: true).isAuthenticated==true? const HomePage(): const LoginRegister()
    );
  }
}