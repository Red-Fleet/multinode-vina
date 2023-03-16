import 'dart:html';

import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/material.dart';
import 'package:ui/services/client_http_service.dart';
import 'package:ui/services/master_http_service.dart';
import 'dart:convert';

class InitiateDockingTab extends StatefulWidget {
  const InitiateDockingTab({super.key});

  @override
  State<InitiateDockingTab> createState() => _InitiateDockingTabState();
}

class _InitiateDockingTabState extends State<InitiateDockingTab> {
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

  /// target file
  String targetFileName = "";
  FileUploadInputElement targetFileInput = FileUploadInputElement();

  /// ligand file
  String ligandFileName = "";
  FileUploadInputElement ligandFileInput = FileUploadInputElement();

  /// submit button
  late bool disableSubmitButton;

  @override
  void initState() {
    super.initState();
    getDetailsFromBackendFlag = true;
    sortOnNameFlag = true;
    sortOnClientIdFlag = false;
    sortOnClientStateFlag = false;
    sortOnRequestStateFlag = false;
    searchFlag = false;
    disableSubmitButton = false;

    /// initializing targetFileInput for uploading target pdbqt
    targetFileInput.multiple = false;
    targetFileInput.accept = '.pdbqt';

    /// Add an event listener to the input element
    targetFileInput.onChange.listen((e) {
      if (targetFileInput.files != null) {
        // Get the selected file
        File file = targetFileInput.files!.first;
        setState(() {
          targetFileName = file.name;
        });
      }
    });

    /// initializing ligandFileInput for uploading ligand pdbqt
    ligandFileInput.multiple = false;
    ligandFileInput.accept = '.pdbqt';

    /// Add an event listener to the input element
    ligandFileInput.onChange.listen((e) {
      if (ligandFileInput.files != null) {
        // Get the selected file
        File file = ligandFileInput.files!.first;
        setState(() {
          ligandFileName = file.name;
        });
      }
    });
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
      /// fetching all requests created by client and excepted by worker
      final response = await MasterHttpService.getAllConnectionRequests();
      clientDetailsList = [];
      if (response.statusCode == 200) {
        List<dynamic> result = jsonDecode(response.body);
        for (var e in result) {
          /// only save accepted requests
          if (e['state'] == "ACCEPTED") {
            ClientDetails client = ClientDetails();
            client.clientId = e['worker_id'];
            client.requestState = e['state'];

            /// fecthing all client details to whom request was shared
            final clientDetailsResponse =
                await ClientHttpService.getCientDetails(
                    {'client_id': client.clientId});
            if (clientDetailsResponse.statusCode == 200) {
              /// client details received
              var clientDetails = jsonDecode(clientDetailsResponse.body);
              client.clientState = clientDetails['state'];
              client.name = clientDetails['name'];
            } else {
              /// if cannot fetch client details
              debugPrint(clientDetailsResponse.body);
              client.clientState = "error";
              client.name = "error";
            }

            clientDetailsList.add(client);
          }
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
      visibleClientDetailsList.sort((a, b) =>
          a.clientId.toLowerCase().compareTo(b.clientId.toLowerCase()));
    }

    if (sortOnNameFlag) {
      visibleClientDetailsList
          .sort((a, b) => a.name.toLowerCase().compareTo(b.name.toLowerCase()));
    }

    if (sortOnClientStateFlag) {
      visibleClientDetailsList.sort((a, b) =>
          a.clientState.toLowerCase().compareTo(b.clientState.toLowerCase()));
    }

    if (sortOnRequestStateFlag) {
      visibleClientDetailsList.sort((a, b) =>
          a.requestState.toLowerCase().compareTo(b.requestState.toLowerCase()));
    }

    // sorting ends

    /// searching
    if (searchFlag) {
      List<ClientDetails> searchedClients = [];

      for (var client in visibleClientDetailsList) {
        if (client.name
            .toLowerCase()
            .contains(searchController.text.toLowerCase())) {
          searchedClients.add(client);
        } else {
          if (client.clientId
              .toLowerCase()
              .contains(searchController.text.toLowerCase())) {
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

  void submitDockingData() async {
    File targetFile = targetFileInput.files!.first;
    final targetFileReader = FileReader();

    targetFileReader.readAsText(targetFile);
    await targetFileReader.onLoad.first;
    String targetFileContent = targetFileReader.result as String;

    File ligandFile = ligandFileInput.files!.first;
    final ligandFileReader = FileReader();

    ligandFileReader.readAsText(ligandFile);
    await ligandFileReader.onLoad.first;
    String ligandFileContent = ligandFileReader.result as String;

    List<String> workerIds = [];
    for (int i = 0; i < clientDetailsList.length; i++) {
      if (clientDetailsList[i].clientSelected == true) {
        workerIds.add(clientDetailsList[i].clientId);
      }
    }

    final response = await MasterHttpService.initiateDocking(
        target: targetFileContent,
        targetName: targetFile.name,
        ligands: ligandFileContent,
        ligandsName: ligandFile.name,
        workerIds: workerIds);

    setState(() {
      disableSubmitButton = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
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
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(30)),
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
    var dropdownButton = DropdownButton(
        items: const [
          DropdownMenuItem(
            value: "name",
            child: Text("Name"),
          ),
          DropdownMenuItem(
            value: "clientId",
            child: Text("Client Id"),
          ),
          DropdownMenuItem(
            value: "clientState",
            child: Text("Client Status"),
          ),
          DropdownMenuItem(
            value: "requestState",
            child: Text("Request Status"),
          ),
        ],
        value: sortOnNameFlag
            ? "name"
            : (sortOnClientIdFlag
                ? "clientId"
                : (sortOnClientStateFlag ? "clientState" : "requestState")),
        onChanged: (val) {
          setState(() {
            sortOnNameFlag = false;
            sortOnClientIdFlag = false;
            sortOnClientStateFlag = false;
            sortOnRequestStateFlag = false;
            if (val == "name") {
              sortOnNameFlag = true;
            } else if (val == "clientId") {
              sortOnClientIdFlag = true;
            } else if (val == "clientState") {
              sortOnClientStateFlag = true;
            } else if (val == "requestState") {
              sortOnRequestStateFlag = true;
            }
          });
        });

    Widget connectedClientsSelectionWidget = FutureBuilder(
        future: initializeVisibleClientDetailsList(),
        builder: (context, snapshot) {
          double sidePad = screenWidth * .02;
          var listViewChildrens = <Widget>[];

          /// add search and sort in list
          //listViewChildrens.add();

          /// add client details in list
          for (var client in visibleClientDetailsList) {
            listViewChildrens.add(Padding(
              padding: EdgeInsets.only(left: sidePad, right: sidePad),
              child: ClientDetailsTile(clientDetails: client),
            ));
          }
          listViewChildrens.add(const SizedBox(
            height: 50,
          ));
          if (snapshot.hasData) {
            bool result = snapshot.data!;
            if (result == true) {
              return ListView(
                children: listViewChildrens,
              );
            } else {
              return const Text("error");
            }
          } else {
            return const CircularProgressIndicator();
          }
        });

    ///card for target file upload
    Card targetFileWidget = Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      //borderRadius: BorderRadius.circular(20),
      child: SizedBox(
        width: screenWidth * 0.8,
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              const Text(
                "Upload Target PDBQT:  ",
                style: TextStyle(fontSize: 16),
              ),
              Text(targetFileName),
              const Spacer(),
              SelectionContainer.disabled(
                child: IconButton(
                  icon: const Icon(Icons.upload_file),
                  onPressed: () {
                    targetFileInput.click();
                  },
                  style: ButtonStyle(
                    foregroundColor:
                        MaterialStateProperty.all<Color>(Colors.black),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );

    ///card for lignad file upload
    Card ligandFileWidget = Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      //borderRadius: BorderRadius.circular(20),
      child: SizedBox(
        width: screenWidth * 0.8,
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              const Text("Upload Ligands PDBQT:  ",
                  style: TextStyle(fontSize: 16)),
              Text(ligandFileName),
              const Spacer(),
              SelectionContainer.disabled(
                child: IconButton(
                  icon: const Icon(Icons.upload_file),
                  onPressed: () {
                    ligandFileInput.click();
                  },
                  style: ButtonStyle(
                    foregroundColor:
                        MaterialStateProperty.all<Color>(Colors.black),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );

    return Expanded(
      child: ListView(
        children: [
          Padding(
            padding: EdgeInsets.fromLTRB(
                screenWidth * 0.1, 10, screenWidth * 0.1, 0),
            child: ligandFileWidget,
          ),
          Padding(
            padding:
                EdgeInsets.fromLTRB(screenWidth * 0.1, 0, screenWidth * 0.1, 0),
            child: targetFileWidget,
          ),
          Padding(
            padding:
                EdgeInsets.fromLTRB(screenWidth * 0.1, 0, screenWidth * 0.1, 0),
            child: Card(
              color: Colors.white,
              elevation: 2,
              shadowColor: Colors.blue,
              //borderRadius: BorderRadius.circular(20),
              child: Column(
                children: [
                  SizedBox(
                    width: screenWidth * 0.8,
                    child: Padding(
                      padding: const EdgeInsets.only(
                          left: 10, right: 10, top: 10, bottom: 10),
                      child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text(
                              "Select Workers: ",
                              style: TextStyle(fontSize: 16),
                            ),
                            SizedBox(
                                width: (screenWidth - 2 * sidePad) * 0.3,
                                child: searchField),
                            Row(
                              children: [
                                const Text(
                                  "Sort",
                                  style: TextStyle(fontWeight: FontWeight.bold),
                                ),
                                const SizedBox(width: 25),
                                dropdownButton
                              ],
                            )
                          ]),
                    ),
                  ),
                  SizedBox(
                    height: screenHeight * 0.4,
                    width: screenWidth * 0.8,
                    child: connectedClientsSelectionWidget,
                  ),
                ],
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(
                screenWidth * 0.4, 10, screenWidth * 0.4, 0),
            child: OutlinedButton(
              onPressed: () {
                if(disableSubmitButton == true) return;

                setState(() {
                  disableSubmitButton = true;
                });
                submitDockingData();
              },
              style: ButtonStyle(
                shape: MaterialStateProperty.all(RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(40))),
                foregroundColor: MaterialStateProperty.all<Color>(Colors.black),
              ),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(0, 10, 0, 10),
                child: disableSubmitButton
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator())
                    : const Text("Submit"),
              ),
            ),
          )
        ],
      ),
    );
  }
}

/// class used by ConnectionRequests for storing client details
class ClientDetails {
  late String name;
  late String clientId;
  late String clientState;
  late String requestState;
  bool isCurrentClient = false;

  /// for selecting client for computation
  bool clientSelected = false;
}

/// class used by ConnectionRequests for showing client details
class ClientDetailsTile extends StatefulWidget {
  final ClientDetails clientDetails;
  const ClientDetailsTile({super.key, required this.clientDetails});

  @override
  State<ClientDetailsTile> createState() => _ClientDetailsTileState();
}

class _ClientDetailsTileState extends State<ClientDetailsTile> {
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Row(
          children: [
            const Text(
              "Name:",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(
              width: 10,
            ),
            Text(widget.clientDetails.name)
          ],
        ),
        subtitle: Column(
          children: [
            Row(
              children: [
                const Text(
                  "Client Id:",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(
                  width: 10,
                ),
                Text(widget.clientDetails.clientId)
              ],
            ),
            Row(
              children: [
                const Text(
                  "Client Status:",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(
                  width: 10,
                ),
                Text(widget.clientDetails.clientState)
              ],
            ),
            Row(
              children: [
                const Text(
                  "Request status:",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(
                  width: 10,
                ),
                Text(widget.clientDetails.requestState)
              ],
            )
          ],
        ),
        trailing: SelectionContainer.disabled(
          child: Checkbox(
            value: widget.clientDetails.clientSelected,
            onChanged: (value) {
              setState(() {
                widget.clientDetails.clientSelected =
                    !widget.clientDetails.clientSelected;
              });
            },
          ),
        ),
      ),
    );
  }
}
