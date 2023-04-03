import 'package:http/http.dart' as http;
import 'dart:convert';

class MasterHttpService{
  // clientAddress stores address of client
  static const String clientAddress = "http://127.0.0.1:7000";

  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };

  
  /// create connection request, body should have worker_id
  static Future<http.Response> createConnectionRequest(var body){
    return http.post(Uri.parse('$clientAddress/master/connectionrequest/create'), headers: headers, body: body);
  }

  /// delete connection request
  static Future<http.Response> deleteConnectionRequest(String workerId){
    var body = jsonEncode({'worker_id': workerId});
    return http.delete(Uri.parse('$clientAddress/master/connectionrequest'), headers: headers, body: body);
  }

  /// get all connection requests of master
  static Future<http.Response> getAllConnectionRequests(){
    return http.get(Uri.parse('$clientAddress/master/connectionrequest'), headers: headers);
  }

  /// initiate docking
  static Future<http.Response> initiateDocking({required String target, required String targetName, required String ligands, required String ligandsName, required List<String> workerIds}){
    var body = json.encode({
      "target": target,
      "target_name": targetName,
      "ligands": ligands,
      "ligands_name": ligandsName,
      "worker_ids": workerIds
    });

    return http.post(Uri.parse('$clientAddress/master/docking/create'), headers: headers, body: body);
  }
}