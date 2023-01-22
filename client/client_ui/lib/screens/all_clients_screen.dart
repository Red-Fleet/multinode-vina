import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:ui/services/client_http_service.dart';
import 'package:ui/widgets/client_details_tile.dart';

class AllClientScreen extends StatefulWidget {
  const AllClientScreen({super.key});

  @override
  State<AllClientScreen> createState() => _AllClientScreenState();
}

class _AllClientScreenState extends State<AllClientScreen> {

  Future<bool> getData() async{
    await Future.delayed(const Duration(seconds: 1));
    try{
      final response = await ClientHttpService.getAllClients();
      if(response.statusCode == 200){
        print(response.body);
        return true;
      }
      else{
        debugPrint(
            "_AllClientScreenState.getData(): statusCode=${response.statusCode}\nerror:${response.body}");
            return false;
      }
    }
    catch (e){
      debugPrint(e.toString());
      return false;
    }
  }

  List<Widget> getListElements(int count){
    List<Widget> arr = <Widget> [];
    double screenWidth = MediaQuery.of(context).size.width;
    double sidePad = screenWidth*.1;

    for(int i=0; i<count; i++) arr.add(Padding(
      padding: EdgeInsets.only(left: sidePad, right: sidePad),
      child: ClientDetailsTile(clientId: "clientI3333333333333333333333333333d", name: "name", status: "online",),
    ));

    return arr;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: getData(),
      builder: (context, snapshot){
      if(snapshot.hasData){
        bool result = snapshot.data!;
        if(result == true){
          return Expanded(
            child: ListView(
              children: getListElements(50),
            ),
          );
        }
        else{
          return Text("error");
        }
      }
      else{
        return const CircularProgressIndicator();
      }
    });
  }
}