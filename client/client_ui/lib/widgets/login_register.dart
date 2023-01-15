import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/server_model.dart';
import 'dart:math';

import 'package:ui/services/client_http_service.dart';

class LoginRegister extends StatefulWidget {
  const LoginRegister({super.key});

  @override
  State<LoginRegister> createState() => _LoginRegisterState();
}

class _LoginRegisterState extends State<LoginRegister> {
  bool register = false;
  TextEditingController serverAddress = TextEditingController();
  TextEditingController username = TextEditingController();
  TextEditingController password = TextEditingController();
  TextEditingController name = TextEditingController();
  bool obscurePassword = true;
  bool disableLoginButton = false;
  bool disableRegisterButton = false;

  @override
  void dispose() {
    // TODO: implement dispose
    serverAddress.dispose();
    username.dispose();
    password.dispose();
    name.dispose();
    super.dispose();
  }

  void resetControllers() {
    serverAddress.text = "http://";
    username.text = "";
    name.text = "";
    password.text = "";
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    resetControllers();
  }

  /// set server address in client backend
  Future<void> setServerAddress() async{
    final provModel = Provider.of<ServerModel>(context, listen: false);
    final addr = serverAddress.text;
    try{
      final response = await ClientHttpService.setServerAddress({'address': addr});
      if(response.statusCode==200 || response.statusCode==201){
      provModel.serverAddress = addr;
      }
      else{
        debugPrint("_LoginRegisterState.setServerAddress: statusCode=${response.statusCode}\nerror:${response.body}");
      }
    }
    catch(e){
      debugPrint(e.toString());
    }
  }

  void login() async{}

  Widget getLoginWidget() {
    return Container(
      //color: Colors.blue,
      width: max(MediaQuery.of(context).size.width / 3, 400),
      child: Column(
        children: [
          SizedBox(
            height: MediaQuery.of(context).size.height / 7,
          ),
          const Text(
            "Log in to Server",
            style: TextStyle(fontWeight: FontWeight.w900, fontSize: 45),
          ),
          const SizedBox(
            height: 50,
          ),
          TextField(
            controller: serverAddress,
            decoration: InputDecoration(
              border:
                  OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
              labelText: 'Server Address',
            ),
          ),
          const SizedBox(
            height: 30,
          ),
          TextField(
            controller: username,
            decoration: InputDecoration(
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
                labelText: 'Username'),
          ),
          const SizedBox(
            height: 30,
          ),
          Row(
            children: [
              Flexible(
                child: TextField(
                  controller: password,
                  obscureText: obscurePassword,
                  decoration: InputDecoration(
                      border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30)),
                      labelText: 'Password',
                      suffixIcon: IconButton(
                          onPressed: () {
                            setState(() {
                              obscurePassword = !obscurePassword;
                            });
                          },
                          icon: Icon(obscurePassword
                              ? Icons.visibility_off
                              : Icons.visibility))),
                ),
              ),
            ],
          ),
          const SizedBox(
            height: 30,
          ),
          SizedBox(
            width: double.infinity,
            height: 40,
            child: OutlinedButton(
              style: ElevatedButton.styleFrom(
                  //backgroundColor: Colors.green,
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  textStyle: const TextStyle(fontSize: 20)),
              child: const Text("Login"),
              onPressed: () async{
                if(disableLoginButton == true) return;
                disableLoginButton = true;
                
                await setServerAddress();
                disableLoginButton = false;
              },
            ),
          ),
          const SizedBox(
            height: 15,
          ),
          Align(
            alignment: Alignment.centerRight,
            child: InkWell(
                onTap: () {
                  setState(() {
                    register = true;
                  });
                },
                child: const Text(
                  "Register",
                  style: TextStyle(color: Colors.blue),
                )),
          )
        ],
      ),
    );
  }

  Widget getRegisterWidget() {
    return Container(
      //color: Colors.blue,
      width: max(MediaQuery.of(context).size.width / 3, 400),
      child: Column(
        children: [
          SizedBox(
            height: MediaQuery.of(context).size.height / 7,
          ),
          const Text(
            "Register to Server",
            style: TextStyle(fontWeight: FontWeight.w900, fontSize: 45),
          ),
          const SizedBox(
            height: 50,
          ),
          TextField(
            controller: serverAddress,
            decoration: InputDecoration(
              border:
                  OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
              labelText: 'Server Address',
            ),
          ),
          const SizedBox(
            height: 30,
          ),
          TextField(
            controller: username,
            decoration: InputDecoration(
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
                labelText: 'Username'),
          ),
          const SizedBox(
            height: 30,
          ),
          Row(
            children: [
              Flexible(
                child: TextField(
                  controller: password,
                  obscureText: obscurePassword,
                  decoration: InputDecoration(
                      border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30)),
                      labelText: 'Password',
                      suffixIcon: IconButton(
                          onPressed: () {
                            setState(() {
                              obscurePassword = !obscurePassword;
                            });
                          },
                          icon: Icon(obscurePassword
                              ? Icons.visibility_off
                              : Icons.visibility))),
                ),
              ),
            ],
          ),
          const SizedBox(
            height: 30,
          ),
          TextField(
            controller: name,
            decoration: InputDecoration(
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
                labelText: 'Name'),
          ),
          const SizedBox(
            height: 30,
          ),
          SizedBox(
            width: double.infinity,
            height: 40,
            child: OutlinedButton(
              style: ElevatedButton.styleFrom(
                  //backgroundColor: Colors.green,
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  textStyle: const TextStyle(fontSize: 20)),
              child: const Text("Register"),
              onPressed: () {
                print(serverAddress.text);
              },
            ),
          ),
          const SizedBox(
            height: 15,
          ),
          Align(
            alignment: Alignment.centerRight,
            child: InkWell(
                onTap: () {
                  setState(() {
                    register = false;
                  });
                },
                child: const Text(
                  "Login",
                  style: TextStyle(color: Colors.blue),
                )),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    disableLoginButton = false;
    disableRegisterButton = false;
    return SingleChildScrollView(
      child: Container(
        alignment: Alignment.center,
        child: register ? getRegisterWidget() : getLoginWidget(),
      ),
    );
  }
}
