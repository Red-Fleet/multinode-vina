import 'package:http/http.dart' as http;

class MasterHttpService{
  // clientAddress stores address of client
  static const String clientAddress = "http://127.0.0.1:7000";

  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };


  /// fetch all clients present on server
  static Future<http.Response> getAllClients(){
    return http.get(Uri.parse('$clientAddress/client/all'), headers: headers);
  }
  
  /// create connection request, body should have worker_id
  static Future<http.Response> createConnectionRequest(var body){
    return http.post(Uri.parse('$clientAddress/master/connectionrequest/create'), headers: headers, body: body);
  }
}