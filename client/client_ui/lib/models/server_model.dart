import 'package:flutter/foundation.dart';

/// class is used to store sever address
class ServerModel extends ChangeNotifier{
  late String _serverAddress;
  bool _isAddressInit = false;

  String get serverAddress{
    return _serverAddress;
  }

  bool get isAddressInit{
    return _isAddressInit;
  }

  set serverAddress(String serverAddress){
    _serverAddress = serverAddress;
    _isAddressInit = true;
    //notifyListeners();
  }
  
}