import 'dart:html';

import 'package:flutter/services.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/material.dart';
import 'package:ui/services/client_http_service.dart';
import 'package:ui/services/master_http_service.dart';
import 'dart:convert';

import 'package:ui/utils.dart';

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

  //////// params ////////////////////////////
  /// scoring function, default value vina
  String paramScoringFunction = "vina";
  /// input for number of cpu, default is 0
  TextEditingController paramCpuController = TextEditingController(text: "0");
  /// input for Random seed, default is 0
  TextEditingController paramRandomSeedController = TextEditingController(text: "0");
  /// input for exhaustiveness, default is 8
  TextEditingController paramExhaustivenessController = TextEditingController(text: "8");
  /// input for number of pose (n_poses), default is 20
  TextEditingController paramNPosesController = TextEditingController(text:"20");
  /// input for Minimal RMSD, default is 1.0
  TextEditingController paramMinimalRMSDController = TextEditingController(text:"1.0");
  /// input for Maximum evaluations, default is 0
  TextEditingController paramMaximumEvaluationsController = TextEditingController(text:"0");
  /// input for center x coordinate
  TextEditingController paramCenterXController = TextEditingController();
  /// input for center y coordinate
  TextEditingController paramCenterYController = TextEditingController();
  /// input for center z coordinate
  TextEditingController paramCenterZController = TextEditingController();
  /// input for size x 
  TextEditingController paramSizeXController = TextEditingController();
  /// input for size y
  TextEditingController paramSizeYController = TextEditingController();
  /// input for size z 
  TextEditingController paramSizeZController = TextEditingController();
  /// input for grid spacing default: 0.375
  TextEditingController paramSpacingController = TextEditingController(text:"0.375");
  

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
      if (targetFileInput.files != null && targetFileInput.files!.isNotEmpty) {
        // Get the selected file
        File file = targetFileInput.files!.first;
        setState(() {
          targetFileName = file.name;
        });
      }
      else{
        setState(() {
          targetFileName = "";
        });
      }
    });

    /// initializing ligandFileInput for uploading ligand pdbqt
    ligandFileInput.multiple = true;
    ligandFileInput.accept = '.pdbqt';

    /// Add an event listener to the input element
    ligandFileInput.onChange.listen((e) {
      if (ligandFileInput.files != null && ligandFileInput.files!.isNotEmpty) {
        // Get the selected file
        File file = ligandFileInput.files!.first;
        String fileNames = "";
        for(file in ligandFileInput.files!) fileNames += file.name + ", ";
        if(fileNames.isNotEmpty) fileNames = fileNames.substring(0, fileNames.length-2); 
        setState(() {
          ligandFileName = fileNames;
        });
      }
      else{
        setState(() {
          ligandFileName = "";
        });
      }
    });
  }

  @override
  void dispose() {
    /// dispose all controllers
    searchController.dispose();
    paramCpuController.dispose();
    paramRandomSeedController.dispose();
    paramExhaustivenessController.dispose();
    paramNPosesController.dispose();
    paramMinimalRMSDController.dispose();
    paramMaximumEvaluationsController.dispose();
    paramCenterXController.dispose();
    paramCenterYController.dispose();
    paramCenterZController.dispose();
    paramSizeXController.dispose();
    paramSizeYController.dispose();
    paramSizeZController.dispose();
    paramSpacingController.dispose();
    super.dispose();
  }

  /////////// Vaidations ////////////////////
  String? paramCpuValidator(String? val){
    if(paramCpuController.text.isEmpty){
      return 'Can\'t be empty';
    }

    return null;
  }

  String? paramRandomSeedValidators(String? val){
    if(paramRandomSeedController.text.isEmpty){
      return 'Can\'t be empty';
    }

    return null;
  }
  
  String? paramExhaustivenessValidators(String? val){
    if(paramExhaustivenessController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isInteger(paramExhaustivenessController.text)==false || getInteger(paramExhaustivenessController.text)! < 1){
      return "Must be greater than 0";
    }

    return null;
  }

  String? paramNPosesValidators(String? val){
    if(paramNPosesController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isInteger(paramNPosesController.text)==false || getInteger(paramNPosesController.text)! < 1){
      return "Must be greater than 0";
    }

    return null;
  }

  String? paramMinimalRMSDValidators(String? val){
    if(paramMinimalRMSDController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramMinimalRMSDController.text)==false){
      return "Must be a number";
    }

    if(getDouble(paramMinimalRMSDController.text)! <= 0){
      return "Must be greater than 0";
    }

    return null;
  }

  String? paramMaximumEvaluationsValidators(String? val){
    if(paramMaximumEvaluationsController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isInteger(paramMaximumEvaluationsController.text)==false || getInteger(paramMaximumEvaluationsController.text)! < 0){
      return "Must be positive";
    }

    return null;
  }

  String? paramCenterXControllerValidators(String? val){
    if(paramCenterXController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramCenterXController.text)==false){
      return "Must be number";
    }

    return null;
  }

  String? paramCenterYControllerValidators(String? val){
    if(paramCenterYController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramCenterYController.text)==false){
      return "Must be number";
    }

    return null;
  }

  String? paramCenterZControllerValidators(String? val){
    if(paramCenterZController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramCenterZController.text)==false){
      return "Must be number";
    }

    return null;
  }

  String? paramSizeXControllerValidators(String? val){
    if(paramSizeXController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramSizeXController.text)==false){
      return "Must be number";
    }

    return null;
  }

  String? paramSizeYControllerValidators(String? val){
    if(paramSizeYController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramSizeYController.text)==false){
      return "Must be number";
    }

    return null;
  }

  String? paramSizeZControllerValidators(String? val){
    if(paramSizeZController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramSizeZController.text)==false){
      return "Must be number";
    }

    return null;
  }

  String? paramSpacingControllerValidators(String? val){
    if(paramSpacingController.text.isEmpty){
      return 'Can\'t be empty';
    }

    if(isDouble(paramSpacingController.text)==false){
      return "Must be number";
    }

    if(getDouble(paramSpacingController.text)!<= 0){
      return "Must be greater than 0";
    }

    return null;
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
            "getClientDetailsFromBackend: statusCode=${response.statusCode}\nerror:${response.body}");
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

    List<String> ligandFileContents = [];
    List<String> ligandsName = [];
    for(var ligandFile in ligandFileInput.files!){
      var ligandFileReader = FileReader();

      ligandFileReader.readAsText(ligandFile);
      await ligandFileReader.onLoad.first;
      ligandFileContents.add(ligandFileReader.result as String);
      ligandsName.add(ligandFile.name);
    }
    
    

    List<String> workerIds = [];
    for (int i = 0; i < clientDetailsList.length; i++) {
      if (clientDetailsList[i].clientSelected == true) {
        workerIds.add(clientDetailsList[i].clientId);
      }
    }
    
    try{
    final response = await MasterHttpService.initiateDocking(
        target: targetFileContent,
        targetName: targetFile.name,
        ligands: ligandFileContents,
        ligandsName: ligandsName,
        cpuNum: getInteger(paramCpuController.text)!,
        randomSeed: getInteger(paramRandomSeedController.text)!,
        scoringFunction: paramScoringFunction,
        exhaustiveness: getInteger(paramExhaustivenessController.text)!,
        maximumEvaluations: getInteger(paramMaximumEvaluationsController.text)!,
        minimalRMSD: getDouble(paramMinimalRMSDController.text)!,
        nPoses: getInteger(paramNPosesController.text)!,
        centerX: getDouble(paramCenterXController.text)!,
        centerY: getDouble(paramCenterYController.text)!,
        centerZ: getDouble(paramCenterZController.text)!,
        sizeX: getDouble(paramSizeXController.text)!,
        sizeY: getDouble(paramSizeYController.text)!,
        sizeZ: getDouble(paramSizeZController.text)!,
        gridSpacing: getDouble(paramSpacingController.text)!,
        workerIds: workerIds);

        
    }
    finally{
          setState(() {
      disableSubmitButton = false;
    });

    }

  }

  void handleParamScoringFunctionChange(String? value) {
    setState(() {
      paramScoringFunction = value!;
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
              Expanded(
                //width: 100,
                child: SingleChildScrollView(
            
            //for horizontal scrolling
            scrollDirection: Axis.horizontal,
            child: Text(ligandFileName)),
              ),
              //const Spacer(),
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

    /// card for vina params
    Card vinaOptions = Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(children: [
          Row(
            children: <Widget>[
              const Expanded(
                child: Text(
                  "Scoring Function:",
                  style: TextStyle(fontSize: 16),
                ),
              ),
              Expanded(
                child: RadioListTile(
                  title: const Text("Vina"),
                  value: "vina",
                  groupValue: paramScoringFunction,
                  onChanged: handleParamScoringFunctionChange,
                ),
              ),
              Expanded(
                child: RadioListTile(
                  title: const Text("Vinardo"),
                  value: "vinardo",
                  groupValue: paramScoringFunction,
                  onChanged: handleParamScoringFunctionChange,
                ),
              ),
              Expanded(
                child: RadioListTile(
                  title: const Text("AD4"),
                  value: "ad4",
                  groupValue: paramScoringFunction,
                  onChanged: handleParamScoringFunctionChange,
                ),
              ),
            ],
          ),
          // number of cpu
          Row(
            children: [
              const Text(
                "Number of CPU to use (Default 0: use all of them): ",
                style: TextStyle(fontSize: 16),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(50, 0, 0, 0),
                child: SizedBox(
                  width: 100, 
                  child: TextFormField(
                      inputFormatters: <TextInputFormatter>[
                        FilteringTextInputFormatter.digitsOnly
                      ], // Only numbers can be entered
                      controller: paramCpuController,
                      decoration: const InputDecoration(
                        isDense: true,
                      ),
                      validator: paramCpuValidator,
                      autovalidateMode: AutovalidateMode.always,),
                ),
              )
            ],
          ),
          const SizedBox(height: 10,),
          /// random seed
          Row(
            children: [
              const Text(
                "Random seed (Default 0: ramdomly choosed): ",
                style: TextStyle(fontSize: 16),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(50, 0, 0, 0),
                child: SizedBox(
                  width: 100, 
                  child: TextFormField(
                      inputFormatters: <TextInputFormatter>[
                        FilteringTextInputFormatter.digitsOnly
                      ], // Only numbers can be entered
                      controller: paramRandomSeedController,
                      decoration: const InputDecoration(
                        isDense: true,
                      ),
                      validator: paramRandomSeedValidators,
                      autovalidateMode: AutovalidateMode.always,),
                ),
              )
            ],
          ),
        ]),
      ),
    );

    /// card for docking params
    Card dockingOptions = Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(children: [
          Row(children: [
            Expanded(
              child: Row(
              children: [
                const Text(
                  "Exhaustiveness: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(50, 0, 0, 0),
                  child: SizedBox(
                    width: 150, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.digitsOnly
                        ], // Only numbers can be entered
                        controller: paramExhaustivenessController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramExhaustivenessValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
          Expanded(
            child: Row(
              children: [
                const Text(
                  "Number of Poses: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(50, 0, 0, 0),
                  child: SizedBox(
                    width: 150, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.digitsOnly
                        ], // Only numbers can be entered
                        controller: paramNPosesController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramNPosesValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
            ),
          ),
          
          ],),

          Row(children: [
            Expanded(
              child: Row(
              children: [
                const Text(
                  "Minimal RMSD: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(50, 0, 0, 0),
                  child: SizedBox(
                    width: 150, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.]'))
                        ], // Only numbers can be entered
                        controller: paramMinimalRMSDController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramMinimalRMSDValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
          Expanded(
            child: Row(
              children: [
                const Text(
                  "Maximum evaluations: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(50, 0, 0, 0),
                  child: SizedBox(
                    width: 150, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.digitsOnly
                        ], // Only numbers can be entered
                        controller: paramMaximumEvaluationsController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramMaximumEvaluationsValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
            ),
          ),
          
          ],)
        
        
        ]),
      ),
    );

    /// card for center, size, spacing
    Card centerSizeSpacingCard = Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(children: [
          /// Center Position
          Row(children: [
            const Expanded(child: Text("Center Position (Angstrom)", style: TextStyle(fontSize: 16),)),
            Expanded(
              child: Row(
              children: [
                const Text(
                  "X: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 0, 0),
                  child: SizedBox(
                    width: 100, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.-]'))
                        ], // Only numbers can be entered
                        controller: paramCenterXController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramCenterXControllerValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
            Expanded(
              child: Row(
              children: [
                const Text(
                  "Y: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 0, 0),
                  child: SizedBox(
                    width: 100, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.-]'))
                        ], // Only numbers can be entered
                        controller: paramCenterYController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramCenterYControllerValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
            Expanded(
              child: Row(
              children: [
                const Text(
                  "Z: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 0, 0),
                  child: SizedBox(
                    width: 100, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.-]'))
                        ], // Only numbers can be entered
                        controller: paramCenterZController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramCenterZControllerValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),

          ],),
          /// Size
          Row(children: [
            const Expanded(child: Text("Box Size (Angstrom)", style: TextStyle(fontSize: 16),)),
            Expanded(
              child: Row(
              children: [
                const Text(
                  "X: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 0, 0),
                  child: SizedBox(
                    width: 100, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.]'))
                        ], // Only numbers can be entered
                        controller: paramSizeXController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramSizeXControllerValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
            Expanded(
              child: Row(
              children: [
                const Text(
                  "Y: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 0, 0),
                  child: SizedBox(
                    width: 100, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.]'))
                        ], // Only numbers can be entered
                        controller: paramSizeYController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramSizeYControllerValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
            Expanded(
              child: Row(
              children: [
                const Text(
                  "Z: ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 0, 0),
                  child: SizedBox(
                    width: 100, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.]'))
                        ], // Only numbers can be entered
                        controller: paramSizeZController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramSizeZControllerValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
            
          ],),
          /// grid spacing
          Row(children: [
            Expanded(
              child: Row(
              children: [
                const Text(
                  "Grid Spacing (default: 0.375): ",
                  style: TextStyle(fontSize: 16),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 0, 0),
                  child: SizedBox(
                    width: 100, 
                    child: TextFormField(
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.allow(RegExp('[0-9.]'))
                        ], // Only numbers can be entered
                        controller: paramSpacingController,
                        decoration: const InputDecoration(
                          isDense: true,
                        ),
                        validator: paramSpacingControllerValidators,
                        autovalidateMode: AutovalidateMode.always,),
                  ),
                )
              ],
                      ),
            ),
          ],)

        ]),
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
            child: vinaOptions,
          ),
          Padding(
            padding:
                EdgeInsets.fromLTRB(screenWidth * 0.1, 0, screenWidth * 0.1, 0),
            child: dockingOptions,
          ),
          Padding(
            padding:
                EdgeInsets.fromLTRB(screenWidth * 0.1, 0, screenWidth * 0.1, 0),
            child: centerSizeSpacingCard,
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
                /// check for validation
                if(paramCpuValidator(null)!=null ||
                paramNPosesValidators(null) != null ||
                paramRandomSeedValidators(null) != null ||
                paramExhaustivenessValidators(null) != null ||
                paramSizeXControllerValidators(null) != null ||
                paramSizeYControllerValidators(null) != null ||
                paramSizeZControllerValidators(null) != null ||
                paramCenterXControllerValidators(null) != null ||
                paramCenterYControllerValidators(null) != null ||
                paramCenterZControllerValidators(null) != null ||
                paramMinimalRMSDValidators(null) != null ||
                paramSpacingControllerValidators(null) != null ||
                paramMaximumEvaluationsValidators(null) != null 
                ) return;
                if (disableSubmitButton == true) return;

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
