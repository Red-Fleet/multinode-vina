import 'dart:js_util';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ui/icons.dart';
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
  TextEditingController serverAddress = TextEditingController();
  TextEditingController clientId = TextEditingController();
  bool disableConnectButton = false;

  @override
  void dispose() {
    // TODO: implement dispose
    serverAddress.dispose();
    clientId.dispose();
    super.dispose();
  }

  void resetControllers() {
    serverAddress.text = "http://";
    clientId.text = "";
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    resetControllers();
    disableConnectButton = false;
  }

  /// set server address in client backend
  Future<void> connect() async {
    final userModel = Provider.of<UserModel>(context, listen: false);
    final messenger = ScaffoldMessenger.of(context);
    final address = serverAddress.text;
    final clientId = this.clientId.text;

    try {
      final body = json.encode(
          {'address': address, 'client_id': clientId});

      final response = await ClientHttpService.connect(body);
      if (response.statusCode == 200 || response.statusCode == 201) {
        final userDetails = jsonDecode(response.body);
        userModel.serverAddress = address;
        userModel.clientId = userDetails['client_id'];
        userModel.isAuthenticated = true;
      } else {
        debugPrint(
            "_LoginRegisterState.connect(): statusCode=${response.statusCode}\nerror:${response.body}");
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
            "Connect to Server",
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
            controller: clientId,
            decoration: InputDecoration(
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
                labelText: 'Username'),
          ),
          const SizedBox(
            height: 30,
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
              child: disableConnectButton == true
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
                if (disableConnectButton == true) return;
                setState(() {
                  disableConnectButton = true;
                });

                await connect();

                setState(() {
                  disableConnectButton = false;
                });
              },
            ),
          ),
          
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Container(
        alignment: Alignment.center,
        child: getLoginWidget(),
      ),
    );
  }
}
