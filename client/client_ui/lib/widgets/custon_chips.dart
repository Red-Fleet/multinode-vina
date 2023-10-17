import 'package:flutter/material.dart';

class CustomChips extends StatelessWidget {
  final int index; // index of chip
  final Function(int) notifyParent; 
  final String label; // label of chip
  final bool selected; // is this chip is selected or not

  const CustomChips({super.key, required this.index, required this.label, required this.notifyParent, required this.selected});

  @override
  Widget build(BuildContext context) {
    return SelectionContainer.disabled(
      child: ActionChip(
            onPressed: (){
              notifyParent(index);
            },
            elevation:5,
            //shape: StadiumBorder(side: BorderSide()),
            label: Text(
              label,
              style: const TextStyle(
                  color: Colors.black),
            ),
            backgroundColor: selected ? Color.fromARGB(80, 0, 0, 0) : Colors.transparent),
    );
  }
}