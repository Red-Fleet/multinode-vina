import 'dart:js_util';

import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:provider/provider.dart';
import 'package:ui/models/user_model.dart';
import 'dart:math';
import 'dart:convert';
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
    disableLoginButton = false;
    disableRegisterButton = false;
  }

  /// set server address in client backend
  Future<void> loginUser() async {
    final userModel = Provider.of<UserModel>(context, listen: false);
    final messenger = ScaffoldMessenger.of(context);
    final address = serverAddress.text;
    final username = this.username.text;
    final password = this.password.text;
    //await Future.delayed(const Duration(seconds: 5));
    try {
      final body = json.encode(
          {'address': address, 'username': username, 'password': password});

      final response = await ClientHttpService.login(body);
      if (response.statusCode == 200 || response.statusCode == 201) {
        final userDetails = jsonDecode(response.body);
        userModel.serverAddress = address;
        userModel.username = username;
        userModel.password = password;
        userModel.clientId = userDetails['client_id'];
        userModel.name = userDetails['name'];
        userModel.isAuthenticated = true;
      } else {
        debugPrint(
            "_LoginRegisterState.login(): statusCode=${response.statusCode}\nerror:${response.body}");
      }

      if (response.statusCode == 500) {
        messenger.showSnackBar(const SnackBar(
            content: Text('Server Address Error'),
            duration: Duration(seconds: 3)));
      }
      if (response.statusCode == 401) {
        messenger.showSnackBar(const SnackBar(
            content: Text('Incorrect Username or Password'),
            duration: Duration(seconds: 3)));
      }
    } catch (e) {
      messenger.showSnackBar(const SnackBar(
            content: Text('Connection Error'),
            duration: Duration(seconds: 3)));
      debugPrint(e.toString());
    }
  }

  Future<void> registerUser() async {
    final userModel = Provider.of<UserModel>(context, listen: false);
    final messenger = ScaffoldMessenger.of(context);
    final address = serverAddress.text;
    final username = this.username.text;
    final password = this.password.text;
    final name = this.name.text;
    //await Future.delayed(const Duration(seconds: 5));
    try {
      final body = json.encode(
          {'address': address, 'username': username, 'password': password, 'name': name});

      final response = await ClientHttpService.register(body);
      if (response.statusCode == 200 || response.statusCode == 201) {
        final userDetails = jsonDecode(response.body);
        userModel.serverAddress = address;
        userModel.username = username;
        userModel.password = password;
        userModel.clientId = userDetails['client_id'];
        userModel.name = name;
        userModel.isAuthenticated = true;
      } else {
        debugPrint(
            "_LoginRegisterState.login(): statusCode=${response.statusCode}\nerror:${response.body}");
      }

      if (response.statusCode == 500) {
        messenger.showSnackBar(const SnackBar(
            content: Text('Server Address Error'),
            duration: Duration(seconds: 3)));
      }
    } catch (e) {
      messenger.showSnackBar(const SnackBar(
            content: Text('Connection Error'),
            duration: Duration(seconds: 3)));
      debugPrint(e.toString());
    }
  }

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
              child: disableLoginButton == true
                  ? Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        SizedBox(
                          width: 30,
                        ),
                        Text("Login"),
                        SizedBox(
                          width: 15,
                        ),
                        SizedBox(
                            height: 15,
                            width: 15,
                            child: CircularProgressIndicator())
                      ],
                    )
                  : const Text("Login"),
              onPressed: () async {
                if (disableLoginButton == true) return;
                setState(() {
                  disableLoginButton = true;
                });

                await loginUser();

                setState(() {
                  disableLoginButton = false;
                });
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
              child: disableRegisterButton == true
                  ? Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        SizedBox(
                          width: 30,
                        ),
                        Text("Register"),
                        SizedBox(
                          width: 15,
                        ),
                        SizedBox(
                            height: 15,
                            width: 15,
                            child: CircularProgressIndicator())
                      ],
                    )
                  : const Text("Register"),
              onPressed: () async{
                if (disableRegisterButton == true) return;
                setState(() {
                  disableRegisterButton = true;
                });

                await registerUser();

                setState(() {
                  disableRegisterButton = false;
                });
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
    return SingleChildScrollView(
      child: Container(
        alignment: Alignment.center,
        child: register ? getRegisterWidget() : getLoginWidget(),
      ),
    );
  }
}
