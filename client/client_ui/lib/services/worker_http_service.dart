import 'dart:html';

import 'package:http/http.dart' as http;
import 'dart:convert';

class WorkerHttpService{
  // clientAddress stores address of client
  static String clientAddress =  window.location.origin;

  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };

  

  /// get all connection requests for worker
  static Future<http.Response> getAllConnectionRequests(){
    return http.get(Uri.parse('$clientAddress/worker/connectionrequest'), headers: headers);
  }

  /// reject connection request
  static Future<http.Response> rejectConnectionRequest(String masterId){
    var body = jsonEncode({
      'master_id': masterId
    });

    return http.put(Uri.parse('$clientAddress/worker/connectionrequest/reject'), body: body, headers: headers);
  }

  /// accept connection request
  static Future<http.Response> acceptConnectionRequest(String masterId){
    var body = jsonEncode({
      'master_id': masterId
    });
    return http.put(Uri.parse('$clientAddress/worker/connectionrequest/accept'), body: body, headers: headers);
  }

}