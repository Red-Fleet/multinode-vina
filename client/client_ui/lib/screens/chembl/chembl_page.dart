import 'package:flutter/material.dart';
import 'package:ui/screens/chembl/pdbqt_download.dart';
import 'package:ui/screens/chembl/sdf_download.dart';
import 'package:ui/widgets/custon_chips.dart';

class ChemblPage extends StatefulWidget {
  const ChemblPage({super.key});

  @override
  State<ChemblPage> createState() => _ChemblPageState();
}

class _ChemblPageState extends State<ChemblPage> {
  var selectedTab = 0; // index of selected tab
  final tabs = ["Download SDF", "Download PDBQT"];

  void changeSelectedTab(int index){
    setState(() {
      selectedTab = index;
    });
  }

  Widget getTabBody(){
    if(selectedTab==0){
      return const SdfDownload();
    }
    if(selectedTab == 1){
      return const PdbqtDownload();
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