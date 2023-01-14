import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'dart:math';

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
    serverAddress.text = "https://";
    username.text = "";
    name.text = "";
    password.text = "";
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    serverAddress.text = "https://";
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
              child: const Text("Login"),
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
    return SingleChildScrollView(
      child: Container(
        alignment: Alignment.center,
        child: register ? getRegisterWidget() : getLoginWidget(),
      ),
    );
  }
}
