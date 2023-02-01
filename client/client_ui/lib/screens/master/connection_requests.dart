import 'dart:html';

import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:ui/services/client_http_service.dart';
import 'package:ui/services/master_http_service.dart';
import 'dart:convert';

class ConnectionRequests extends StatefulWidget {
  const ConnectionRequests({super.key});

  @override
  State<ConnectionRequests> createState() => _ConnectionRequestsState();
}



class _ConnectionRequestsState extends State<ConnectionRequests> {
  /// client details from backend will be stored here
  List<ClientDetails> clientDetailsList = [];

  /// final client details which will be shown to the user
  List<ClientDetails> visibleClientDetailsList = [];

  /// Flags
  /// true = fetch client details from backend, false dont fetch
  late bool getDetailsFromBackendFlag;

  /// sort clients based on name
  late bool sortOnNameFlag;

  /// sort clients based on state
  late bool sortOnClientStateFlag;

  /// sort client based of state of request
  late bool sortOnRequestStateFlag;

  /// sort clients based on clientId
  late bool sortOnClientIdFlag;

  /// search on name and clientId
  late bool searchFlag;
  TextEditingController searchController = TextEditingController();


  @override
  void initState() {
    super.initState();
    getDetailsFromBackendFlag = true;
    sortOnNameFlag = true;
    sortOnClientIdFlag = false;
    sortOnClientStateFlag = false;
    sortOnRequestStateFlag = false;
    searchFlag = false;
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  /// Get client details to whom connection request was send
  /// return list contaning client details
  Future<bool> getClientDetailsFromBackend() async {
    try {
      /// fetching all requests created by client
      final response = await MasterHttpService.getAllConnectionRequests();
      clientDetailsList = [];
      if (response.statusCode == 200) {
        List<dynamic> result = jsonDecode(response.body);
        for (var e in result) {
          ClientDetails client = ClientDetails();
          client.clientId = e['worker_id'];
          client.requestState = e['state'];
          /// fecthing all client details to whom request was shared
          final clientDetailsResponse = await ClientHttpService.getCientDetails({'client_id':client.clientId});
          if(clientDetailsResponse.statusCode == 200){
            /// client details received
            var clientDetails = jsonDecode(clientDetailsResponse.body);
            client.clientState = clientDetails['state'];
            client.name = clientDetails['name'];
          }
          else{
            /// if cannot fetch client details
            debugPrint(clientDetailsResponse.body);
            client.clientState = "error";
            client.name = "error";
          }
          
          clientDetailsList.add(client);
        }
        return true;
      } else {
        debugPrint(
            "_AllClientTabState.getData(): statusCode=${response.statusCode}\nerror:${response.body}");
        return false;
      }
    } catch (e) {
      debugPrint(e.toString());
      return false;
    }
  }

  /// This method will create final list of client which will be displayed to user
  /// will return false if cannot get client details from backend, else true
  Future<bool> initializeVisibleClientDetailsList() async {
    if (getDetailsFromBackendFlag == true) {
      bool backendCallSuccess;
      backendCallSuccess = await getClientDetailsFromBackend();
      if (backendCallSuccess == false) return false;
    }

    visibleClientDetailsList = [];
    for (var e in clientDetailsList) {
      visibleClientDetailsList.add(e);
    }

    /// sorting start
    if (sortOnClientIdFlag) {
      visibleClientDetailsList.sort((a, b) => a.clientId.toLowerCase().compareTo(b.clientId.toLowerCase()));
    }

    if (sortOnNameFlag) {
      visibleClientDetailsList.sort((a, b) => a.name.toLowerCase().compareTo(b.name.toLowerCase()));
    }

    if (sortOnClientStateFlag) {
      visibleClientDetailsList.sort((a, b) => a.clientState.toLowerCase().compareTo(b.clientState.toLowerCase()));
    }

    if (sortOnRequestStateFlag) {
      visibleClientDetailsList.sort((a, b) => a.requestState.toLowerCase().compareTo(b.requestState.toLowerCase()));
    }

    // sorting ends

    /// searching
    if (searchFlag) {
      List<ClientDetails> searchedClients = [];

      for (var client in visibleClientDetailsList) {
        if (client.name.toLowerCase().contains(searchController.text.toLowerCase())) {
          searchedClients.add(client);
        } else {
          if (client.clientId.toLowerCase().contains(searchController.text.toLowerCase())) {
            searchedClients.add(client);
          }
        }
      }

      visibleClientDetailsList = searchedClients;
    }

    /// reset all flags
    getDetailsFromBackendFlag = false;
    // sortOnClientIdFlag = false;
    // sortOnNameFlag = true;
    // sortOnStateFlag = false;
    searchFlag = false;

    return true;
  }

  /// This method is used to delete connection request from server
  void deleteConnectionRequest(String workerId) async{
    final messenger = ScaffoldMessenger.of(context);
    try{
      final response = await MasterHttpService.deleteConnectionRequest(workerId=workerId);
      
      if(response.statusCode != 200){
        debugPrint(
            "statusCode=${response.statusCode}\nerror:${response.body}");
        
        messenger.showSnackBar(const SnackBar(
            content: Text('Backend Error'),
            duration: Duration(seconds: 3)));
      }
      else{
         messenger.showSnackBar(const SnackBar(
            content: Text('Connection Request Deleted'),
            duration: Duration(seconds: 3)));
        
        setState(() {
          getDetailsFromBackendFlag = true;
        });
      }


    }
    catch(e){
      debugPrint(e.toString());

      messenger.showSnackBar(const SnackBar(
            content: Text('Error'),
            duration: Duration(seconds: 3)));
    }

  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: initializeVisibleClientDetailsList(),
        builder: (context, snapshot) {
          var listViewChildrens = <Widget>[];
          double screenWidth = MediaQuery.of(context).size.width;
          double sidePad = screenWidth * .1;

          /// search field
          var searchField = TextField(
            controller: searchController,
            onSubmitted: (val) {
              setState(() {
                searchFlag = true;
              });
            },
            
            decoration: InputDecoration(
              isDense: true,
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
                labelText: 'Search',
                suffixIcon: IconButton(
                    onPressed: () {
                      setState(() {
                        searchFlag = true;
                      });
                    },
                    icon: const Icon(Icons.search))),
          );

          /// sort field
          var dropdownButton = DropdownButton(items: const [
            DropdownMenuItem(value: "name",child: Text("Name"),),
            DropdownMenuItem(value: "clientId",child: Text("Client Id"),),
            DropdownMenuItem(value: "clientState",child: Text("Client Status"),),
            DropdownMenuItem(value: "requestState",child: Text("Request Status"),),
          ],
          value: sortOnNameFlag?"name":(sortOnClientIdFlag?"clientId":(sortOnClientStateFlag?"clientState":"requestState")),
           onChanged: (val){
            setState(() {
            sortOnNameFlag = false;
            sortOnClientIdFlag = false;
            sortOnClientStateFlag = false;
            sortOnRequestStateFlag = false;
            if(val == "name"){
              sortOnNameFlag = true;
            }
            else if(val == "clientId"){
              sortOnClientIdFlag = true;
            }
            else if(val == "clientState"){
              sortOnClientStateFlag = true;
            }
            else if(val == "requestState"){
              sortOnRequestStateFlag = true;
            }
            });

          });
          
          /// add search and sort in list
          listViewChildrens.add(Padding(
            padding: EdgeInsets.only(left: sidePad, right: sidePad, top:10, bottom: 10),
            child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween,children: [SizedBox(width: (screenWidth-2*sidePad)*0.4,child: searchField), Row(children: [Text("Sort", style: TextStyle(fontWeight: FontWeight.bold),), SizedBox(width:25), dropdownButton],)]),
          ));

          /// add client details in list
          for (var client in visibleClientDetailsList) {
            listViewChildrens.add(Padding(
              padding: EdgeInsets.only(left: sidePad, right: sidePad),
              child: ClientDetailsTile(
                clientDetails: client,
                deleteButtonNotifyParent: deleteConnectionRequest,
              ),
            ));
          }
          listViewChildrens.add(const SizedBox(height: 50,));
          if (snapshot.hasData) {
            bool result = snapshot.data!;
            if (result == true) {
              return Expanded(
                child: ListView(
                  children: listViewChildrens,
                ),
              );
            } else {
              return Text("error");
            }
          } else {
            return const CircularProgressIndicator();
          }
        });
  }
}

/// class used by ConnectionRequests for storing client details
class ClientDetails {
  late String name;
  late String clientId;
  late String clientState;
  late String requestState;
  bool isCurrentClient = false;
}

/// class used by ConnectionRequests for showing client details
class ClientDetailsTile extends StatelessWidget {
  final ClientDetails clientDetails;
  /// notify parent when delete button is pressed
  final Function(String) deleteButtonNotifyParent;
  const ClientDetailsTile({super.key, required this.clientDetails, required this.deleteButtonNotifyParent});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Row(children: [const Text("Name:", style: TextStyle(fontWeight: FontWeight.bold),), const SizedBox(width: 10,), Text(clientDetails.name)],),
        subtitle: Column(
          children: [
            Row(children: [const Text("Client Id:", style: TextStyle(fontWeight: FontWeight.bold),), const SizedBox(width: 10,), Text(clientDetails.clientId)],),
            Row(children: [const Text("Client Status:", style: TextStyle(fontWeight: FontWeight.bold),), const SizedBox(width: 10,), Text(clientDetails.clientState)],),
            Row(children: [const Text("Request status:", style: TextStyle(fontWeight: FontWeight.bold),), const SizedBox(width: 10,), Text(clientDetails.requestState)],)
          ],
        ),
        trailing: SelectionContainer.disabled(child: ElevatedButton(child: const Text("Delete"), style: ButtonStyle(backgroundColor: MaterialStatePropertyAll<Color>(Colors.red)),onPressed: (){
          deleteButtonNotifyParent(clientDetails.clientId);
        })),
      ),
    );
  }
}