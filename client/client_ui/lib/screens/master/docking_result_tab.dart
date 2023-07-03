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

  Future<bool> initializeDockingIds() async {
    if (getDockingIdsFromBackendFlag == true) {
      final response = await MasterHttpService.getMasterDockingIds();

      if (response.statusCode == 200) {
        List<dynamic> result = jsonDecode(response.body);
        for (dynamic data in result) {
          dockingIdsWithStatus.add({
            "docking_id": data['docking_id'],
            "state": data['state'],
            'computed': data['computed']
          });
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
        for (Map dockingDetails in dockingIdsWithStatus) {
          DockingTile tile = DockingTile(
              dockingId: dockingDetails['docking_id'],
              state: dockingDetails['state'],
              computedLigandsCount: dockingDetails['computed']);
          listChildren.add(tile);
        }
        return Flexible(
          child: Padding(
            padding: EdgeInsets.fromLTRB(
                screenWidth * 0.1, 10, screenWidth * 0.1, 20),
            child: ListView(
              children: listChildren,
            ),
          ),
        );
      },
    );
  }
}

class DockingTile extends StatefulWidget {
  String dockingId;
  String state;
  int computedLigandsCount;

  DockingTile(
      {super.key,
      required this.dockingId,
      required this.state,
      required this.computedLigandsCount});

  @override
  State<DockingTile> createState() => _DockingTileState();
}

class _DockingTileState extends State<DockingTile> {
  /// if downloading is true then disable downloading butten
  bool downloading = false;
  /// for storing download path
  TextEditingController downloadPathController = TextEditingController();

  Future<void> saveDockingResult()async{
    final response =  await MasterHttpService.saveDockingResult(widget.dockingId, downloadPathController.text);

    if(response.statusCode == 200 || response.statusCode == 201){
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
            content: Text('Downloaded'),
            duration: Duration(seconds: 3)));
    
    }
    else{
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            content: Text('Error while Downloading (${response.body})'),
            duration: Duration(seconds: 7)));
    }
  }

  AlertDialog getDialog(){
    return AlertDialog(
      content: Row(
        children: [
          const Text("Download Path: "),
          Expanded(
            child: TextFormField(
              controller: downloadPathController,
              decoration: const InputDecoration(
                                isDense: true,
                              ),
              
            ),
          ),
        ],
      ),
      actions: [
        ElevatedButton(
          onPressed: () async{
            // removid alert box
            Navigator.pop(context);
            // turning off download button
            setState(() {
                  downloading = true;
                });

            // downloading
            await saveDockingResult();

            // turning on download button
            setState(() {
                  downloading = false;
                });

          },
          child: const Text("Submit")),
      ],
      actionsAlignment: MainAxisAlignment.center
    );
  }
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
            Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  const Text("Docking Id : ",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(widget.dockingId)
                ],
              ),
              const SizedBox(
                height: 5,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  const Text("State : ",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(widget.state),
                ],
              ),
              const SizedBox(
                height: 5,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  const Text("Ligands Docked: ",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(widget.computedLigandsCount.toString())
                ],
              )
            ]),
            const Expanded(
              child: SizedBox(),
            ),
            downloading? const SizedBox(
                    height: 20.0,
                    width: 20.0,
                    child: Center(
                      child: CircularProgressIndicator(strokeWidth: 2,)
                    ),
                  ):
            ElevatedButton(
                onPressed: () async {
                
                  
                  showDialog(
                    context: context,
                    builder: (BuildContext context) {
                      return getDialog();
                    },
                  );
                  //// start from here
                },
                child: const Text("Download Result"))
            //Column(children: [const Expanded(child: SizedBox(),), ElevatedButton(onPressed: (){}, child: const Text("Download")), const Expanded(child: SizedBox(),)],)
          ],
        ),
      ),
    );
  }
}
