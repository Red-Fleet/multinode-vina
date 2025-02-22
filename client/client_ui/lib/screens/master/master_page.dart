import 'package:flutter/material.dart';
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
  final tabs = ["Initiate Docking", "Result"];

  void changeSelectedTab(int index){
    setState(() {
      selectedTab = index;
    });
  }

  Widget getTabBody(){
    if(selectedTab==0){
      return const InitiateDockingTab();
    }
    if(selectedTab == 1){
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