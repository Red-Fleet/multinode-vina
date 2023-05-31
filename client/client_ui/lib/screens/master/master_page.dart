import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:ui/screens/master/all_clients_tab.dart';
import 'package:ui/screens/master/connected_clients.dart';
import 'package:ui/screens/master/connection_requests.dart';
import 'package:ui/screens/master/docking_result_tab.dart';
import 'package:ui/screens/master/initiate_docking_tab.dart';
import 'package:ui/widgets/custon_chips.dart';

class MasterPage extends StatefulWidget {
  const MasterPage({super.key});

  @override
  State<MasterPage> createState() => MasterPageState();
}

class MasterPageState extends State<MasterPage> {
  var selectedTab = 0; // index of selected tab
  final tabs = ["All Clients", "Connection Requests","Connected Clients", "Initiate Docking", "Result"];

  void changeSelectedTab(int index){
    setState(() {
      selectedTab = index;
    });
  }

  Widget getTabBody(){
    if(selectedTab==0){
      return const AllClientTab();
    }
    if(selectedTab == 1){
      return const ConnectionRequests();
    }
    if(selectedTab==2){
      return const ConnectedClients();
    }
    if(selectedTab==3){
      return const InitiateDockingTab();
    }
    if(selectedTab == 4){
      return const DockingResultTab();
    }

    return Container();
  }

  @override
  Widget build(BuildContext context) {
    final toolBar = <Widget>[];
    for (int i = 0; i < tabs.length; i++) {
      toolBar.add(Padding(
        padding: const EdgeInsets.only(left: 10, right: 10),
        child: CustomChips(index: i, label: tabs[i], notifyParent: changeSelectedTab, selected: selectedTab==i),
      ));
    }
    return Column(
      children: [
        SizedBox(
          width: MediaQuery.of(context).size.width,
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Padding(
              padding:const EdgeInsets.only(left: 50, right: 50, top: 10, bottom: 15),
              child: Row(
                children:toolBar,
              ),
            ),
          ),
        ),

        getTabBody()
      ],
    );
  }
}