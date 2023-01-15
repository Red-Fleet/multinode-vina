import 'package:http/http.dart' as http;
import 'dart:convert';

class ClientHttpService{
  // clientAddress stores address of client
  static const String clientAddress = "http://127.0.0.1:7000";

  // api for storing server address in client
  static const String serverAddressApi = "server/address";

  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };

  static Future<http.Response> setServerAddress(var body){
    return http.post(Uri.parse('$clientAddress/$serverAddressApi'), body: json.encode(body), headers: headers);
  }

  // static Future<http.Response> login(String server){
  //   return null;
  // }
}