import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:ui/globals.dart' as globals;


class ChemblHttpService{
  // clientAddress stores address of client
  static String clientAddress =  globals.clientAddress;

  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };


  
  static Future<http.Response> sdfDownload(String chemblId, String path){
    print(clientAddress);
    print("######################################");
    var body = json.encode({
      "chembl_id": chemblId,
      "dir_path": path
    });

    return http.post(Uri.parse('$clientAddress/chembl/save/sdf'), headers: headers, body: body);
  }

  static Future<http.Response> pdbqtDownload(String chemblId, String path){
    var body = json.encode({
      "chembl_id": chemblId,
      "dir_path": path
    });

    return http.post(Uri.parse('$clientAddress/chembl/save/pdbqt'), headers: headers, body: body);
  }
}