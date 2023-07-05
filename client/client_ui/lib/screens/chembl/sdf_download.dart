import 'package:flutter/material.dart';
import 'package:ui/services/chembl_http_service.dart';

class SdfDownload extends StatefulWidget {
  const SdfDownload({super.key});

  @override
  State<SdfDownload> createState() => _SdfDownloadState();
}

class _SdfDownloadState extends State<SdfDownload> {
  TextEditingController downloadPathController = TextEditingController();
  TextEditingController chembelIdsController = TextEditingController();

  /// submit button
  late bool disableSubmitButton = false;


  Future<void> downloadSdfs() async{
    List<String> ids = chembelIdsController.text.split(RegExp(r'[,\s\n\t]+'));
    String path = downloadPathController.text;
    var messenger = ScaffoldMessenger.of(context);
    for(var id in ids)
    {
      final response = await ChemblHttpService.sdfDownload(id, path);
      if(response.statusCode != 200){
        messenger.showSnackBar(
         SnackBar(
            content: Text('Download failed ($id): ${response.body}'),
            duration: Duration(seconds: 3)));
      }
    }

    messenger.showSnackBar(
         const SnackBar(
            content: Text('Download finisded'),
            duration: Duration(seconds: 3)));
    
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
    double sidePad = screenWidth * .1;

    // download path card
    Card downloadPathCard = Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      //borderRadius: BorderRadius.circular(20),
      child: SizedBox(
        width: screenWidth * 0.8,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(8, 20, 8, 20),
          child: Row(
            children: [
              const Text(
                "Download path:     ",
                style: TextStyle(fontSize: 16),
              ),
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
        ),
      ),
    );

    Card chembelIdsCard = 
    Card(
      color: Colors.white,
      elevation: 2,
      shadowColor: Colors.blue,
      //borderRadius: BorderRadius.circular(20),
      child: SizedBox(
        width: screenWidth * 0.8,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(8, 20, 8, 20),
          child: Row(
            children: [
              const Text(
                "Chembl Ids (space, tab, newline, comma seprated):     ",
                style: TextStyle(fontSize: 16),
              ),
              Expanded(
                child: TextFormField(
              controller: chembelIdsController,
              keyboardType: TextInputType.multiline,
              minLines: 1,
              maxLines: 8,
              decoration: const InputDecoration(
                                  isDense: true,
                                ),
              
              
            ),
              ),
              
            ],
          ),
        ),
      ),
    );

    Widget downloadButton =  OutlinedButton(
              onPressed: () async{
                
                if (disableSubmitButton == true) return;

                setState(() {
                  disableSubmitButton = true;
                });
                await downloadSdfs();
                setState(() {
                  disableSubmitButton = false;
                });

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
                    : const Text("Download"),
              ),
            );
          

    return Expanded(
                child: Padding(
                  padding: EdgeInsets.fromLTRB(
                  screenWidth * 0.1, 20, screenWidth * 0.1, 20),
                  child: ListView(
                    children: [
                      
            downloadPathCard, 
            chembelIdsCard,
            
            Padding(
            padding: EdgeInsets.fromLTRB(
                  screenWidth * 0.3, 20, screenWidth * 0.3, 0),
            child: downloadButton)
                    ],
                  ),
                ));
  }
}