import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ui/icons.dart';
import 'package:ui/models/user_model.dart';

class UserAvatar extends StatefulWidget {
  const UserAvatar({super.key});

  @override
  State<UserAvatar> createState() => _UserAvatarState();
}

class _UserAvatarState extends State<UserAvatar> {
  @override
  Widget build(BuildContext context) {
    return PopupMenuButton(
      icon: const Icon(MyIcons.person),
      itemBuilder: (BuildContext context) {
        return [

          PopupMenuItem(
            child: Row(children: [
              const Text('Username :', style: TextStyle(
                fontWeight: FontWeight.bold
              ),),
              const SizedBox(width: 10,),
              Flexible(child: Text(Provider.of<UserModel>(context, listen: false).clientId, overflow: TextOverflow.ellipsis))
            ]),
          ),
        ];
      },
    );
  }
}
