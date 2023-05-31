import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/material.dart';
import 'package:ui/services/master_http_service.dart';

class DockingResultTab extends StatefulWidget {
  const DockingResultTab({super.key});

  @override
  State<DockingResultTab> createState() => _DockingResultTabState();
}

class _DockingResultTabState extends State<DockingResultTab> {
  late bool getDockingIdsFromBackendFlag;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    getDockingIdsFromBackendFlag = true;
  }

  Future<bool> initializeDockingIds() async{
    if(getDockingIdsFromBackendFlag == true){
      final response = await MasterHttpService.getMasterDockingIds();
    }



    /// reset flag
    getDockingIdsFromBackendFlag = false;
    return true;
  }

  @override
  Widget build(BuildContext context) {
    if(getDockingIdsFromBackendFlag == true){
      
    }
    return FutureBuilder(
      future: initializeDockingIds(),
      builder: (context, snapshot) {

      },
      );
  }
}