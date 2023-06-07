import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:ui/services/master_http_service.dart';

class DockingResultTab extends StatefulWidget {
  const DockingResultTab({super.key});

  @override
  State<DockingResultTab> createState() => _DockingResultTabState();
}

class _DockingResultTabState extends State<DockingResultTab> {
  late bool getDockingIdsFromBackendFlag;

  List<Map> dockingIdsWithStatus = [];

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    getDockingIdsFromBackendFlag = true;
  }

  Future<bool> initializeDockingIds() async{
    if(getDockingIdsFromBackendFlag == true){
      final response = await MasterHttpService.getMasterDockingIds();

      if (response.statusCode == 200) {
        List<dynamic> result = jsonDecode(response.body);
        for(dynamic data in result){
          dockingIdsWithStatus.add({"docking_id": data['docking_id'], "state": data['state'], 'computed': data['computed']});
        }
      }
    }


    /// reset flag
    getDockingIdsFromBackendFlag = false;
    return true;
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    return FutureBuilder(
      future: initializeDockingIds(),
      builder: (context, snapshot) {
        
        List<Widget> listChildren = [];
        for(Map dockingDetails in dockingIdsWithStatus){
          DockingTile tile = DockingTile(dockingId: dockingDetails['docking_id'], state: dockingDetails['state'], computedLigandsCount: dockingDetails['computed']);
          listChildren.add(tile);
        }
        return Flexible(
          child: Padding(
            padding: EdgeInsets.fromLTRB(screenWidth*0.1, 10, screenWidth*0.1, 20),
            child: ListView(
              children: listChildren,
            ),
          ),
        );
      },
      );
  }
}

class DockingTile extends StatelessWidget {
  String dockingId;
  String state;
  int computedLigandsCount;
  DockingTile({super.key, required this.dockingId, required this.state, required this.computedLigandsCount});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: 
            [
              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                const Text("Docking Id : ", style: TextStyle(fontWeight: FontWeight.bold)),
                Text(dockingId)
              ],),

              const SizedBox(height: 5,),

              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  const Text("State : ", style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(state),
                ],
              ),
              const SizedBox(height: 5,),

              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  const Text("Legands Docked: ", style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(computedLigandsCount.toString())
                ],
              )

              
            ]),
            const Expanded(child: SizedBox(),),
            ElevatedButton(onPressed: (){}, child: const Text("Download Result"))
            //Column(children: [const Expanded(child: SizedBox(),), ElevatedButton(onPressed: (){}, child: const Text("Download")), const Expanded(child: SizedBox(),)],)
          ],
        ),
      ),

    );
  }
}