import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:ui/globals.dart' as globals;

class MasterHttpService{
  // clientAddress stores address of client
  static String clientAddress =  globals.clientAddress;

  static const Map<String, String> headers = {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
    // "Access-Control-Allow-Methods":"DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    };

  

  /// initiate docking
  static Future<http.Response> initiateDocking({required String target, 
  required String targetName, 
  required List<String> ligands, 
  required List<String> ligandsName,
  required String scoringFunction,
  required int cpuNum,
  required int randomSeed,
  required int exhaustiveness,
  required int nPoses,
  required double minimalRMSD,
  required int maximumEvaluations,
  required double centerX,
  required double centerY,
  required double centerZ,
  required double sizeX,
  required double sizeY,
  required double sizeZ,
  required double gridSpacing,
  required List<String> workerIds}){
    var body = json.encode({
      "target": target,
      "target_name": targetName,
      "ligands": ligands,
      "ligands_name": ligandsName,
      "scoring_function": scoringFunction,
      "cpu_num": cpuNum,
      "random_seed": randomSeed,
      "exhaustiveness": exhaustiveness,
      "n_poses": nPoses,
      "min_rmsd": minimalRMSD,
      "max_evals": maximumEvaluations,
      "center_x": centerX,
      "center_y": centerY,
      "center_z": centerZ,
      "box_size_x": sizeX,
      "box_size_y": sizeY,
      "box_size_z": sizeZ,
      "grid_spacing": gridSpacing,
      "worker_ids": workerIds
    });

    return http.post(Uri.parse('$clientAddress/master/docking/create'), headers: headers, body: body);
  }


  /// get all dockings started by user
  static Future<http.Response> getMasterDockingIds(){
    return http.get(Uri.parse('$clientAddress/master/docking/ids'), headers: headers);
  }

  /// save docking result
  static Future<http.Response> saveDockingResult(String dockingId, String path){
    var body = json.encode({
      "docking_id": dockingId,
      "path": path
    });

    return http.post(Uri.parse('$clientAddress/master/docking/result/download'), headers: headers, body: body);
  }

  /// delete docking
  static Future<http.Response> deleteDocking(String dockingId){
    var body = json.encode({
      "docking_id": dockingId
    });
    return http.delete(Uri.parse('$clientAddress/master/docking/delete'), headers: headers, body: body);
  }
}