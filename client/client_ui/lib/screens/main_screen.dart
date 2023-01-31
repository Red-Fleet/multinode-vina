import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/user_model.dart';
import 'package:ui/services/client_http_service.dart';
import 'package:ui/screens/login_register.dart';
import 'package:ui/screens/master/master_page.dart';
import 'package:ui/widgets/user_avatar.dart';
import 'dart:convert';

import 'package:ui/screens/worker_page.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final GlobalKey<ScaffoldState> _drawerscaffoldkey =
      GlobalKey<ScaffoldState>();

  bool masterSeleted = true;

  void initUser() async {
    try {
      final userModel = Provider.of<UserModel>(context, listen: false);
      final response = await ClientHttpService.getUserDetails();

      if (response.statusCode == 200) {
        final userDetails = jsonDecode(response.body);
        userModel.username = userDetails['username'];
        userModel.name = userDetails['name'];
        userModel.clientId = userDetails['client_id'];
        userModel.password = userDetails['password'];
        userModel.isAuthenticated = true;
      }
    } catch (e) {
      debugPrint(e.toString());
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    initUser();
    masterSeleted = true;
  }

  @override
  Widget build(BuildContext context) {
    return SelectionArea(
      child: Scaffold(
          appBar: AppBar(
            title: const Text("Multinode Vina"),
            backgroundColor: Colors.black,
            leading: Provider.of<UserModel>(context, listen: true).isAuthenticated ==
                        true?IconButton(
              onPressed: () {
                if (_drawerscaffoldkey.currentState!.isDrawerOpen) {
                  //if drawer is open, then close the drawer
                  Navigator.pop(context);
                } else {
                  _drawerscaffoldkey.currentState!.openDrawer();
                  //if drawer is closed then open the drawer.
                }
              },
              icon: const Icon(Icons.menu),
            ):null,
            actions:
                Provider.of<UserModel>(context, listen: true).isAuthenticated ==
                        true
                    ? [const UserAvatar()]
                    : [],
          ),
          body: Scaffold(
            key: _drawerscaffoldkey,
            drawer:
                Provider.of<UserModel>(context, listen: true).isAuthenticated ==
                        true
                    ? Drawer(
                      backgroundColor: Colors.black,
                        child: ListView(
                          children: [
                              const SizedBox(height: 40,),
                              ListTile(hoverColor: const Color.fromARGB(43, 255, 255, 255),
                                selected: masterSeleted,
                                selectedTileColor: const Color.fromARGB(138, 255, 255, 255),
                                title: const Center(child: Text("Master", style:TextStyle(color: Colors.white))), onTap: (){
                                    setState(() {
                                      masterSeleted = true;
                                    });
                                    Navigator.pop(context);
                              },),
                              const SizedBox(height: 10,),
                               ListTile(
                                selected: !masterSeleted,
                                selectedTileColor: const Color.fromARGB(138, 255, 255, 255),
                                hoverColor: const Color.fromARGB(43, 255, 255, 255),
                                title: const Center(child: Text("Worker", style:TextStyle(color: Colors.white))), onTap: (){
                                    setState(() {
                                      masterSeleted = false;
                                    });
                                    Navigator.pop(context);
                               },),
                            ],
                        ),
                    )
                    : null,
            body: Provider.of<UserModel>(context, listen: true).isAuthenticated ==
                    true
                ? (masterSeleted?const MasterPage(): const WorkerPage())
                : const LoginRegister(),
          )),
    );
  }
}
