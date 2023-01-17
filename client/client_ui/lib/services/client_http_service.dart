import 'package:http/http.dart' as http;

class ClientHttpService{
  // clientAddress stores address of client
  static const String clientAddress = "http://127.0.0.1:7000";

  // api for storing server address in client
  static const String loginApi = "user/login";
  static const String registerApi = "user/register";
  static const String userDetailsApi = "user/details";
  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };

  static Future<http.Response> login(var body){
    return http.post(Uri.parse('$clientAddress/$loginApi'), body: body, headers: headers);
  }

  static Future<http.Response> register(var body){
    return http.post(Uri.parse('$clientAddress/$registerApi'), body: body, headers: headers);
  }

  static Future<http.Response> getUserDetails(){
    return http.get(Uri.parse('$clientAddress/$userDetailsApi'), headers: headers);
  }

  // static Future<http.Response> login(String server){
  //   return null;
  // }
}