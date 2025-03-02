import 'package:http/http.dart' as http;
import 'package:ui/globals.dart' as globals;

class ClientHttpService{
  // clientAddress stores address of client
  static String clientAddress =  globals.clientAddress;

  // api for storing server address in client
  static const String connectApi = "user/connect";
  static const String userDetailsApi = "user/details";
  static const String getAllClientsApi = "client/all";

  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };

  static Future<http.Response> connect(var body){
    return http.post(Uri.parse('$clientAddress/$connectApi'), body: body, headers: headers);
  }

  static Future<http.Response> getUserDetails(){
    return http.get(Uri.parse('$clientAddress/$userDetailsApi'), headers: headers);
  }

  /// fetch all clients present on server
  static Future<http.Response> getAllClients(){
    return http.get(Uri.parse('$clientAddress/client/all'), headers: headers);
  }

  /// fetch all detrails of single client present on server
  static Future<http.Response> getCientDetails(var queryParameters){
    var path = Uri.http(clientAddress.replaceAll('http://', ''), '/client/details', queryParameters);
    return http.get(path, headers: headers);
  }
}